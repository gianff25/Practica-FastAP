from asyncio import run
from functools import wraps

import typer

from apps.users.models import UserDB
from utils.auth import hash_password


# This is a standard decorator that takes arguments
# the same way app.command does but with
# app as the first parameter
def async_command(app, *args, **kwargs):
    def decorator(async_func):
        # Now we make a function that turns the async
        # function into a synchronous function.
        # By wrapping async_func we preserve the
        # meta characteristics typer needs to create
        # a good interface, such as the description and
        # argument type hints
        @wraps(async_func)
        def sync_func(*_args, **_kwargs):
            return run(async_func(*_args, **_kwargs))

        # Now use app.command as normal to register the
        # synchronous function
        app.command(*args, **kwargs)(sync_func)

        # We return the async function unmodifed,
        # so its library functionality is preserved
        return async_func

    return decorator


# as a method injection, app will be replaced as self
# making the syntax exactly the same as it used to be.
# put this all in __init__.py and it will be injected into
# the library project wide
typer.Typer.async_command = async_command


app = typer.Typer()


@app.async_command()
async def seed_database():
    print("Seeding database...")


@app.async_command()
async def seed_user():
    user = {
        "username": "admin",
        "password": hash_password("admin"),
        "email": "admin@example.com",
        "is_staff": True,
        "is_active": True,
    }
    await UserDB.create_async(**user)


def __main__():
    app()


if __name__ == "__main__":
    __main__()
