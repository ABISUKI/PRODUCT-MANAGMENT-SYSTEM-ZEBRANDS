import time
import uuid
import bcrypt

from api.app.entities.exceptions import UserNotUpdated, UserAlreadyExistError, DataNotFoundError, WrongCredentialsError
from api.app.entities.persistence_models import UserCreationPersistenceModel
from api.ports.db_port_interface import DBMainInterface


class Users:
    def __init__(self, db: DBMainInterface):
        self.db = db
        self.__user_collection = "users"

    @staticmethod
    def user_doc_model(
        doc_id: str,
        user_name: str,
        group_id: str,
        role_ids: list[str],
        email: str,
        password: str
    ) -> dict:
        time_ = int(time.time() * 1000)
        return UserCreationPersistenceModel(
            id=doc_id,
            user_name=user_name,
            password=password,
            group_id=group_id,
            role_ids=role_ids,
            email=email,
            update_at=time_,
            created_at=time_,
            modified_by=None,
        ).dict()

    def create_user(self, user_name: str, group_id: str, role_ids: list[str], email: str, password: str, **kwargs):
        results = self.db.query(collection=self.__user_collection, filters=[("email", "==", email)])
        if results:
            user_id = results[0].get("id")
            raise UserAlreadyExistError(f"User Already exist: UserId: {user_id}")

        doc_id = str(uuid.uuid4())
        hash_pwd = self.hash_password(password)
        document_data = self.user_doc_model(
            doc_id, user_name, group_id, role_ids, email, hash_pwd
        )
        self.db.create(
            collection="users", document_id=doc_id, document_data=document_data
        )
        return document_data

    def update_user(self, user_id: str, user_name: str = None, group_id: str = None, role_ids: list[str] = None, email: str = None, **kwargs):
        doc_to_update = {}
        document_data = {"user_name": user_name, "group_id": group_id, "role_ids": role_ids, "email": email}
        for field in document_data:
            if document_data.get(field):
                doc_to_update.update({field: document_data.get(field)})
            else:
                continue
        time_ = int(time.time() * 1000)
        if not doc_to_update:
            raise UserNotUpdated("User not updated, Theres is not fields to updated")

        doc_to_update.update({"updated_at": time_})
        self.db.update(
            collection=self.__user_collection, document_id=user_id, document_data=doc_to_update
        )
        return {"updated": doc_to_update}

    def delete_user(self, user_id: str, **kwargs):
        self.db.delete(collection=self.__user_collection, document_id=user_id)
        print("Deleted!")
        return {}

    def get_all_users(self):
        return {"users": self.db.get_all(self.__user_collection)}

    def get_user_by_id(self, user_id: str):
        user_doc = self.db.get(collection=self.__user_collection, document_id=user_id)
        if not user_doc:
            raise DataNotFoundError(f"User Id: {user_id} not found!")
        return {"user": self.db.get(collection=self.__user_collection, document_id=user_id)}

    @staticmethod
    def hash_password(pwd: str) -> str:
        bytes_pwd = pwd.encode("utf-8")
        salt = bcrypt.gensalt()
        hash_pwd = bcrypt.hashpw(bytes_pwd, salt).decode("utf-8")
        return hash_pwd
