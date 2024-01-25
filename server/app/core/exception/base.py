from typing import Any
from http import HTTPStatus
from fastapi import status, HTTPException


class CustomException(HTTPException):
    status_code: int
    message: str
    error: dict[str:Any]

    def __init__(self, status_code=None, message=None, error=None):
        if status_code:
            self.status_code = status_code
        if message:
            self.message = message
        if error:
            self.error = error
        super().__init__(status_code=self.status_code, detail=error)


class BadRequestException(CustomException):
    status_code = HTTPStatus.BAD_REQUEST
    message = "Error in request"
    error = {"errors": ["Error in request"]}


class ConnectionException(CustomException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = "Error connecting to database"
    error = {"connection": ["Error connecting to database"]}


class NotFoundException(CustomException):
    status_code = HTTPStatus.NOT_FOUND
    message = "Data not found"
    error = {"errors": ["Data not found"]}


class ForbiddenException(CustomException):
    status_code = HTTPStatus.FORBIDDEN
    message = "User does not have access"
    error = {"errors": ["User does not have access"]}


class UnauthorizedException(CustomException):
    status_code = HTTPStatus.UNAUTHORIZED
    message = "Authorization Error"
    error = {"errors": ["User does not have access"]}


class UnprocessableEntity(CustomException):
    status_code = HTTPStatus.UNPROCESSABLE_ENTITY
    message = "Validation Error"
    error = {"errors": "Validation Error"}


class AuthenticationRequiredException(CustomException):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = "Authentication Required"
    error = {"errors": ["Authentication Required"]}


class AuthenticationFailedException(CustomException):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = "Authentication failed"
    error = {"errors": ["Authentication failed"]}


class TooManyRequestException(CustomException):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    message = "The number of requests has exceeded the limit. Please try again later"
    error = {}


class LogicException(CustomException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = "Error in processing"
    error = {}


class NotActiveException(CustomException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = "Data not available"
    error = {}
