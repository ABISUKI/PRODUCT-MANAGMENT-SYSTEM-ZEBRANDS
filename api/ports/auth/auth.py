import functools
import os
import traceback

import jwt
from fastapi import Request
from bcrypt import checkpw
from datetime import datetime, timedelta

from api.app.entities.exceptions import UserNotFound, WrongCredentialsError
from api.ports.db_port_interface import DBMainInterface


class BarerTokenExpired(Exception):
    """Raised when ..."""
    pass


class InvalidBearerToken(Exception):
    """Raised when ..."""
    pass


class AccessDenied(Exception):
    """Raised when ..."""
    pass


class AuthLayerError(Exception):
    """Raised when ..."""
    pass


class Auth:

    def __init__(self, db: DBMainInterface):
        self.db = db
        self.__user_collection = "users"

    def login(self, email: str, pwd: str):
        results = self.db.query(collection=self.__user_collection, filters=[("email", "==", email)])
        if not results:
            raise UserNotFound(f"User: {email} not found. Please use email as user field")
        doc = results[0]
        self.__validate_password(sent_password=pwd, current_hash=doc.get("password"))
        data = {"hash_id": doc.get("password"),
                "role_id": "root",
                "user_id": doc.get("id")}
        return self.create_access_token(data)

    @classmethod
    def create_access_token(cls, data: dict) -> str:
        to_encode = data.copy()

        # expire time of the token
        expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, os.getenv("SECRET_KEY", "something-secret"), algorithm="HS256")
        # return the generated token
        return encoded_jwt

    @classmethod
    def __validate_password(cls, sent_password: str, current_hash: str) -> None:
        bytes_sent_password: bytes = sent_password.encode("utf-8")
        bytes_current_hash: bytes = current_hash.encode("utf-8")
        if not checkpw(bytes_sent_password, bytes_current_hash):
            raise WrongCredentialsError(f"Wrong password.")

    @staticmethod
    def check_access_admin(func):
        """Exception handler for controller service logic"""
        role_names = ["ADMIN_SUPER_ACCESS"]

        @functools.wraps(func)
        async def handler(*args, **kwargs):
            try:
                token = kwargs.get("token")
                request: Request = kwargs.get("request")
                db: DBMainInterface = kwargs.get("db_firestore")
                token_doc: dict = Auth.decode_jwt(token.credentials)
                if not token_doc.get("exp"):
                    raise InvalidBearerToken("Invalid bearer token format")
                user_id = token_doc.get("user_id")
                user_doc = db.get(collection="users", document_id=user_id)
                if not user_doc:
                    raise InvalidBearerToken("Invalid bearer token")
                user_role_ids = user_doc.get("role_ids", [])
                roles = [db.get(collection="roles", document_id=role_id) for role_id in user_role_ids]
                print("los roles: ", roles)
                reference_access = [referenece for role in roles
                                    for referenece in role.get("reference_access", []) if role if role.get("role_name") in role_names]
                if not reference_access:
                    raise AccessDenied("Access Denied for this API - request the required permissions")
                if request.method in reference_access:
                    return await func(*args, **kwargs)
                raise AccessDenied("Access Denied for this API - request the required permissions")
            except jwt.exceptions.DecodeError as error:
                print(traceback.format_exc())
                raise InvalidBearerToken("Invalid bearer token format: ", str(error))

        return handler

    @staticmethod
    def check_access_api(func):
        """Exception handler for controller service logic"""
        role_names = ["ADMIN_SUPER_ACCESS", "API_V1_ACCESS_ROOT"]

        @functools.wraps(func)
        async def handler(*args, **kwargs):
            token = kwargs.get("token")
            request: Request = kwargs.get("request")
            db: DBMainInterface = kwargs.get("db_firestore")
            token_doc: dict = Auth.decode_jwt(token.credentials)
            if not token_doc.get("exp"):
                raise InvalidBearerToken("Invalid bearer token format")
            user_id = token_doc.get("user_id")
            user_doc = db.get(collection="users", document_id=user_id)
            if not user_doc:
                raise InvalidBearerToken("Invalid bearer token")
            user_role_ids = user_doc.get("role_ids", [])
            roles = [db.get(collection="roles", document_id=role_id) for role_id in user_role_ids]
            reference_access = [referenece for role in roles
                                for referenece in role.get("reference_access", []) if role if
                                role.get("role_name") in role_names]
            if not reference_access:
                raise AccessDenied("Access Denied for this API - request the required permissions")
            if request.method in reference_access:
                return await func(*args, **kwargs)
            raise AccessDenied("Access Denied for this API - request the required permissions")

        return handler

    @staticmethod
    def decode_jwt(token: str) -> dict:
        try:
            decoded_token = jwt.decode(token, os.getenv("SECRET_KEY", "something-secret"), algorithms=["HS256"])
        except Exception as error:
            raise InvalidBearerToken("Invalid bearer token: ", str(error))
        return decoded_token
