from abc import ABCMeta, abstractmethod
from typing import List


class DBMainInterface(metaclass=ABCMeta):

    @abstractmethod
    def create(self, collection: str, document_id: str, document_data: dict):
        pass

    @abstractmethod
    def update(self, collection: str, document_id: str, document_data: dict):
        pass

    @abstractmethod
    def delete(self, collection: str, document_id: str):
        pass

    @abstractmethod
    def get(self, collection: str, document_id: str):
        pass

    @abstractmethod
    def query(self, collection: str, filters: List[tuple], limit: int):
        pass

    @abstractmethod
    def get_all(self, collection: str) -> List[dict]:
        pass

    @abstractmethod
    def get_doc_reference(self, collection: str, document_id: str):
        pass
