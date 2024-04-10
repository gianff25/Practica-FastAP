from typing import Optional

from fastapi import Depends, HTTPException, Request, status
from jose import JWTError, jwt
from passlib.context import CryptContext

from apps.auth.exceptions import AuthException
from apps.auth.models import TokenDB
from apps.auth.schemas.token import TokenData
from apps.users.models import UserDB
from configs.settings import settings
from dependencies.context.user import UserContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def permission_required(
    request: Request, token: str = Depends(settings.OAUTH2_SCHEME)
):
    user = await get_authenticated_user_from_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se pudo validar el token",
        )
    permission = request.state.permission

    if not await user.has_perm(permission):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para acceder a este recurso",
        )
    return user


async def get_current_user(token: str = Depends(settings.OAUTH2_SCHEME)):
    """
    Get the current authenticated user from the provided token.

    args:
        token (str): The token obtained from the request headers.

    returns:
        UserDB: The currently authenticated user obtained from the token.

    raises:
        AuthException: If there is an authentication error or the token is invalid.
    """
    return await get_authenticated_user_from_token(token)


async def get_current_active_user(current_user: UserDB = Depends(get_current_user)):
    """
    Get the current active authenticated user.

    args:
        current_user (UserDB): The currently authenticated user.

    teturns:
        UserDB: The currently authenticated user.

    note:
        This function can be used to ensure that only active users are allowed to access certain routes.
    """
    return current_user


async def get_authenticated_user_from_token(token) -> Optional[UserDB]:
    """
    Get the authenticated user from the provided token.

    args:
        token (str): The token obtained from the request headers.

    returns:
        UserDB: The authenticated user obtained from the token.

    raises:
        AuthException: If there is an authentication error or the token is invalid.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")

        token = (await TokenDB.where_async(token=token)).first()
        if not token:
            raise AuthException().get_exception(1)

        token_data = TokenData(username=username)

        user = (await UserDB.where_async(username=token_data.username)).first()
        if user is None:
            raise AuthException().get_exception(1)

        UserContext.set_user(user)
        return user
    except JWTError:
        token_temp = (await TokenDB.where_async(token=token)).first()
        if token_temp:
            await token_temp.delete_async(token)

    except Exception as e:
        raise AuthException().get_exception(1)


class RequestPermission:
    def __init__(self, value: str):
        self.value = value

    async def __call__(self, request: Request):
        request.state.permission = self.value
