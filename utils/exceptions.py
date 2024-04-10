import json

from fastapi import HTTPException, status

from dependencies.context.exception import ExceptionContext
from dependencies.context.request import RequestContext


class BaseException(Exception, RequestContext):
    def __init__(
        self,
        status_code: int = None,
        message: str = None,
        type: str = None,
        field_name: str = None,
    ):
        self.status_code = status_code
        self.message = message
        self.type = type
        self.field_location = field_name
        if field_name:
            self.field_location = self.find_field_location(field_name)

    def find_field_location(self, field_name: str) -> str:
        try:
            body = self.request.json()
            if field_name in body:
                return field_name
            else:
                for key, value in body.items():
                    if isinstance(value, dict):
                        nested_location = self.find_field_location(value, field_name)
                        if nested_location:
                            return f"{key}.{nested_location}"
        except Exception as e:
            pass
        return None

    def __str__(self) -> str:
        detail = {
            "status_code": self.status_code,
            "message": self.message,
            "location": self.field_location,
            "type": self.type,
        }
        # Filter out None values
        detail = {key: value for key, value in detail.items() if value is not None}
        return json.dumps(detail)


class BaseExceptionHandler(ExceptionContext):
    def __init__(
        self,
        exceptions: dict[int, HTTPException] = {},
        default_exception: HTTPException = None,
    ):
        """
        Initialize the BaseException class.

        :param exceptions: A dictionary containing custom HTTP exceptions, keyed by their respective status codes.
        :param default_exception: A default HTTP exception to use when no specific exception is found for a given status code.
        """
        self.exceptions = exceptions
        self.exceptions.update(self._build_default_exceptions())
        # Default exception for unknown keys
        self.default_exception = default_exception or HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error - Undefined exception",
        )

    # Corrected to be an instance method
    def _build_default_exceptions(self) -> dict[int, HTTPException]:
        """
        Build default HTTP exceptions.

        :return: A dictionary containing default HTTP exceptions.
        """
        # Define your exceptions
        return {
            400: HTTPException(400, "Bad Request"),
            401: HTTPException(401, "Unauthorized"),
            403: HTTPException(403, "Forbidden"),
            404: HTTPException(404, "Not Found"),
            500: HTTPException(500, "Internal Server Error"),
        }
        # Add more exceptions as needed

    # In case you want a function to retrieve exceptions by key
    def get_exception(self, exception_key: int) -> HTTPException:
        """
        Retrieve an HTTP exception by key.

        :param exception_key: The status code of the HTTP exception to retrieve.
        :return: The corresponding HTTP exception, or the default exception if no specific one is found.
        """
        exception = self.exceptions.get(exception_key, self.default_exception)
        return exception
