import functools
import traceback
from pydantic import ValidationError

import logging

from api.app.entities.exceptions import UserNotUpdated, UserAlreadyExistError, DataNotFoundError, WrongCredentialsError, \
    UserNotFound
from api.ports.auth.auth import InvalidBearerToken, AccessDenied, AuthLayerError
from api.ports.firestore.db_main import DBDocumentNotFound, DBInvalidQuery, DBDocumentAlreadyExists
from api.utils.response import Response, Status
from jwt.exceptions import ExpiredSignatureError
from google.api_core.exceptions import AlreadyExists


class ControllerExceptionHandler(object):
    """Decorator class to handle service exceptions"""

    @staticmethod
    def users_creation(func):
        """Exception handler for controller service logic"""

        @functools.wraps(func)
        async def handler(*args, **kwargs):
            response = Response()
            response_root = kwargs.get("response_root")
            try:
                response_root.status_code = 201
                results = await func(*args, **kwargs)
                response.set_response(Status.OK, results)
            except ValidationError as err:
                logging.error(err)
                response.add_error(str(err.errors()))
                response.set_response(Status.BAD_REQUEST, {})
                response_root.status_code = Status.BAD_REQUEST.value
            except UserAlreadyExistError as err:
                logging.error(err)
                response.add_error(str(err.message))
                response.set_response(Status.BAD_REQUEST, {})
                response_root.status_code = Status.BAD_REQUEST.value
            except WrongCredentialsError as err:
                logging.error(err)
                response.add_error(str(err.message))
                response.set_response(Status.FAILED, {})
                response_root.status_code = 401
            except (ExpiredSignatureError, InvalidBearerToken, AccessDenied, AuthLayerError) as err:
                logging.error(err)
                response.add_error(str(err))
                response.set_response(Status.FAILED, {})
                response_root.status_code = 401
            except Exception as err:
                err_details = str(traceback.format_exc())
                logging.error(err)
                logging.error(err_details)
                response.add_error(err_details)
                response.set_response(Status.FAILED, {})
                response_root.status_code = Status.FAILED.value
                response_root.status_code = 500
            return response.result

        return handler

    @staticmethod
    def users(func):
        """Exception handler for controller service logic"""

        @functools.wraps(func)
        async def handler(*args, **kwargs):
            response = Response()
            response_root = kwargs.get("response_root")
            try:
                response_root.status_code = 200
                results = await func(*args, **kwargs)
                response.set_response(Status.OK, results)
            except ValidationError as err:
                logging.error(err)
                response.add_error(str(err.errors()))
                response.set_response(Status.BAD_REQUEST, {})
                response_root.status_code = Status.BAD_REQUEST.value
            except UserNotUpdated as err:
                logging.error(err)
                response.add_error(str(err.message))
                response.set_response(Status.FAILED, {})
                response_root.status_code = Status.FAILED.value
            except (DBDocumentNotFound, DataNotFoundError, UserNotFound) as err:
                logging.error(err)
                response.add_error(str(err.message))
                response.set_response(Status.NOT_FOUND, {})
                response_root.status_code = Status.NOT_FOUND.value
            except DBInvalidQuery as err:
                logging.error(err)
                response.add_error(str(err.message))
                response.set_response(Status.FAILED, {})
                response_root.status_code = Status.FAILED.value
            except WrongCredentialsError as err:
                logging.error(err)
                response.add_error(str(err.message))
                response.set_response(Status.FAILED, {})
                response_root.status_code = 401
            except (ExpiredSignatureError, InvalidBearerToken, AccessDenied, AuthLayerError) as err:
                logging.error(err)
                response.add_error(str(err))
                response.set_response(Status.FAILED, {})
                response_root.status_code = 401
            except Exception as err:
                err_details = str(traceback.format_exc())
                logging.error(err)
                logging.error(err_details)
                response.add_error(err_details)
                response.set_response(Status.FAILED, {})
                response_root.status_code = Status.FAILED.value
                response_root.status_code = 500
            return response.result

        return handler

    @staticmethod
    def products(func):
        """Exception handler for controller service logic"""

        @functools.wraps(func)
        async def handler(*args, **kwargs):
            response = Response()
            response_root = kwargs.get("response_root")
            try:
                response_root.status_code = 200
                results = await func(*args, **kwargs)
                response.set_response(Status.OK, results)
            except ValidationError as err:
                logging.error(err)
                response.add_error(str(err.errors()))
                response.set_response(Status.BAD_REQUEST, {})
                response_root.status_code = Status.BAD_REQUEST.value
            except WrongCredentialsError as err:
                logging.error(err)
                response.add_error(str(err.message))
                response.set_response(Status.FAILED, {})
                response_root.status_code = 401
            except DBDocumentAlreadyExists as err:
                logging.error(err)
                response.add_error(str(err.message))
                response.set_response(Status.BAD_REQUEST, {})
                response_root.status_code = Status.BAD_REQUEST.value
            except (DBDocumentNotFound, DataNotFoundError) as err:
                logging.error(err)
                response.add_error(str(err.message))
                response.set_response(Status.NOT_FOUND, {})
                response_root.status_code = Status.NOT_FOUND.value
            except (ExpiredSignatureError, InvalidBearerToken, AccessDenied, AuthLayerError) as err:
                logging.error(err)
                response.add_error(str(err))
                response.set_response(Status.FAILED, {})
                response_root.status_code = 401
            except Exception as err:
                err_details = str(traceback.format_exc())
                logging.error(err)
                logging.error(err_details)
                response.add_error(err_details)
                response.set_response(Status.FAILED, {})
                response_root.status_code = Status.FAILED.value
                response_root.status_code = 500
            return response.result

        return handler
