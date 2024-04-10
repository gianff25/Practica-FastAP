from fastapi import HTTPException, status

from utils.exceptions import BaseExceptionHandler


class AuthException(BaseExceptionHandler):
    """Exception class for handling authentication-related errors."""

    def __init__(self):
        """
        Initialize the AuthException class.
        """
        exceptions = self._build_exceptions()
        super().__init__(exceptions)

    def _build_exceptions(self) -> dict[int, HTTPException]:
        """
        Build exceptions dictionary.

        returns:
            dict[int, HTTPException]: A dictionary mapping exception codes to HTTPException instances.
        """
        # Define your exceptions
        return {
            # Credentials exceptions for authentication
            1: HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Failed to validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            ),
            # Expired token exception
            2: HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Your token has expired, please log in again",
                headers={"WWW-Authenticate": "Bearer"},
            ),
            # Incorrect username or password for token services
            3: HTTPException(422, "Incorrect username or password"),
        }
