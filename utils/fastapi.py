from contextlib import contextmanager
from typing import Generator

from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError


@contextmanager
def ensure_request_validation_errors() -> Generator[None, None, None]:
    """
    Converter for `ValidationError` to `RequestValidationError`.

    This will convert any ValidationError's inside the called code into
    RequestValidationErrors which will trigger HTTP 422 responses in
    FastAPI. This is useful for when you want to do extra validation in
    your code that is not covered by FastAPI's normal request parameter
    handling.

    Usage examples:

    ```python
    # Use as a context manager
    with ensure_request_validation_errors():
        some_code_doing_extra_validation()  # for example async validation
    ```
    """

    try:
        yield
    except ValidationError as O_o:
        errors = []
        for error in O_o.errors():
            full_msg = error["msg"]
            if "validation error for" in full_msg or "validation errors for" in full_msg:
                msg_errors = full_msg.split("]")
                for i in range(0, len(msg_errors) - 1):
                    loc = (
                        msg_errors[i]
                        .split("\n  ")[0]
                        .split(" ")[-1]
                        .split("\n")[-1]
                        .split(".")
                    )
                    loc_split = []
                    for e in loc:
                        if e == "":
                            continue
                        if e == "body":
                            continue
                        if e.isdigit():
                            loc_split.append(int(e))
                        else:
                            loc_split.append(e)

                    errors.append(
                        {
                            "type": msg_errors[i].split("[type=")[1].split(",")[0],
                            "loc": tuple(loc_split),
                            "msg": msg_errors[i].split("\n  ")[1].split(" [")[0],
                            "input": error["input"],
                        }
                    )
                continue

            errors.append(error)
        raise RequestValidationError(errors=errors) from O_o
