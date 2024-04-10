from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from apps.auth.schemas.token import TokenResponse
from apps.auth.services.token import TokenService
from apps.users.schemas.user import Credential
from dependencies.database import get_db

auth_router = APIRouter()


@auth_router.post("/token", response_model=TokenResponse)
async def open_api_token(
    item: OAuth2PasswordRequestForm = Depends(), db: get_db = Depends()
):
    user = Credential(username=item.username, password=item.password)
    return await TokenService().create(user)
