import time
from enum import Enum


class Status(Enum):
    OK = 200
    NOT_FOUND = 404
    FAILED = 500
    BAD_REQUEST = 400


class Response:
    def __init__(self):
        self.errors = []
        self.result = {}

    def set_response(self, status: Status, results: dict):
        self.result = {"status": status.name, "result": results, "errors": self.errors, "timestamp": int(time.time()* 1000)}
        return self.result

    def add_error(self, error: str):
        self.errors.append(error)
