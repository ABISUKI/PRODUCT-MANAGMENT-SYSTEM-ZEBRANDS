import functools
import os
from typing import List

from google.cloud import firestore as gcp_firestore
from google.api_core.exceptions import NotFound, AlreadyExists
from api.ports.db_port_interface import DBMainInterface


class DBServiceError(Exception):
    """Raise when service has an error"""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class DBMissingCredentials(DBServiceError):
    """Raised when ..."""
    pass


class DBInvalidQuery(DBServiceError):
    """Raised when ..."""
    pass


class DBDocumentNotFound(DBServiceError):
    """Raised when ..."""
    pass


class DBDocumentAlreadyExists(DBServiceError):
    """Raised when ..."""
    pass


class DBMainExceptionHandler(object):
    """Class with handler tools"""

    @staticmethod
    def root(func):
        @functools.wraps(func)
        def handler(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except NotFound as error:
                raise DBDocumentNotFound(str(error))
            except AlreadyExists as error:
                raise DBDocumentAlreadyExists(str(error))

        return handler


class DBMainFirestore(DBMainInterface):

    def __init__(self, service_account_path=None, project_id=None):
        if not service_account_path:
            service_account_path = os.getenv("GOOGLE_CREDENTIALS")

        if not service_account_path:
            raise DBMissingCredentials("Credentials not found!")
        self.project_id = project_id

        kwargs = {}
        if project_id is not None:
            kwargs.update({
                'project': project_id
            })
        if service_account_path is not None:
            from google.oauth2 import service_account as sa

            cred_gcp = sa.Credentials.from_service_account_file(service_account_path, scopes=[
                "https://www.googleapis.com/auth/cloud-platform"])
            kwargs.update({
                'credentials': cred_gcp
            })

            if self.project_id is None:
                self.project_id = cred_gcp.project_id

                if 'project_id' not in kwargs:
                    kwargs.update({
                        'project': self.project_id
                    })

        self.db_client = gcp_firestore.Client(**kwargs)
        self.db_transaction = self.db_client.transaction()

    def get_db_client(self):
        return self.db_client

    def get_doc_reference(self, collection: str, document_id: str):
        return self.db_client.document(f"{collection}/{document_id}")

    @DBMainExceptionHandler.root
    def create(self, collection: str, document_id: str, document_data: dict):
        self.db_client.document(f"{collection}/{document_id}").create(document_data)

    @DBMainExceptionHandler.root
    def update(self, collection: str, document_id: str, document_data: dict):
        self.db_client.document(f"{collection}/{document_id}").update(document_data)

    @DBMainExceptionHandler.root
    def delete(self, collection: str, document_id: str):
        self.db_client.collection(collection).document(document_id).delete()

    def get(self, collection: str, document_id: str) -> dict:
        doc_ref = self.db_client.collection(collection).document(document_id)
        doc = doc_ref.get()
        doc = doc.to_dict()
        return doc if doc else {}

    def query(self, collection: str, filters: list, limit: int = 500) -> List[dict]:
        try:
            if not isinstance(filters, list):
                raise DBInvalidQuery("ERROR: Filter must to be a list of tuples")
            query_ref = self.db_client.collection(collection)
            for _filter in filters:
                if len(_filter) != 3:
                    raise DBInvalidQuery("ERROR: Filter statement must to be composed by 3 elements example: ('name', "
                                         "'==','neftali')")
                query_ref = query_ref.where(*_filter)

            query_ref = query_ref.limit(limit)
            result = [query.to_dict() for query in query_ref.stream()]
            return result

        except Exception as error:
            print(error)
            raise error

    def get_all(self, collection: str) -> List[dict]:
        docs = self.db_client.collection(collection).stream()
        return [doc.to_dict() for doc in docs]
