class ServiceError(Exception):
    """Raise when service has an error"""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class DataNotFoundError(ServiceError):
    """Raised when the there is not dta from DB"""

    pass


class UserAlreadyExistError(ServiceError):
    """Raised when ..."""

    pass


class UserNotFound(ServiceError):
    """Raised when ..."""

    pass


class UserNotUpdated(ServiceError):
    """Raised when ..."""

    pass


class WrongCredentialsError(ServiceError):
    """Raised when ..."""

    pass
