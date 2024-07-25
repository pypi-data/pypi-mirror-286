from typing import Optional
from fastapi import HTTPException


class ApiError(HTTPException):

    error_key: str = "api_error"
    status_code: int = 500

    def __init__(self, message: Optional[str] = None):
        super(ApiError, self).__init__(status_code=self.status_code, detail=message)


class AuthenticationError(ApiError):
    status_code = 401
    error_key = "auth_error"

    def __init__(self, message: str = "you must be authenticated first") -> None:
        super().__init__(message)


class ConfigurationError(SystemExit):
    error_key = "configuration_error"


class Forbidden(ApiError):
    error_key = "forbidden"
    status_code = 403


class BadRequest(ApiError):
    error_key = "bad_request"
    status_code = 400


class Conflict(ApiError):
    error_key = "conflict"
    status_code = 409


class IntegrityError(ApiError):
    error_key = "integrity_error"
    status_code = 409


class NotFound(ApiError):
    error_key = "not_found"
    status_code = 404


class InternalServerError(ApiError):
    error_key = "intrnl_error"
    status_code = 500
