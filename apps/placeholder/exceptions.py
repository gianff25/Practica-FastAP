from utils.exceptions import BaseException, BaseExceptionHandler


class PlaceholderException(
    BaseExceptionHandler,
):
    """Exception class for handling authentication-related errors."""

    def __init__(self):
        """
        Initialize the AuthException class.
        """
        exceptions = self._build_exceptions()
        super().__init__(exceptions)

    def _build_exceptions(self) -> dict[int, BaseException]:
        """
        Build exceptions dictionary.

        returns:
            dict[int, BaseException]: A dictionary mapping exception codes to HTTPException instances.
        """
        # Define your exceptions
        return {
            # Test Exception
            10222: BaseException(
                status_code=10222, message="Test Exception", type="TestException"
            ),
        }
