from datetime import timedelta

from apps.auth.exceptions import AuthException
from apps.auth.repository import AuthRepository
from apps.auth.schemas.token import TokenResponse
from apps.users.repository import UserRepository
from apps.users.services.user import UserService
from configs.settings import settings
from utils.auth import create_access_token, verify_password
from utils.services import BaseService


class TokenService(BaseService):
    def __init__(self, current_user=None):
        super().__init__(current_user=current_user)
        self.repo = AuthRepository(current_user=current_user)
        self.user_repo = UserRepository(current_user=current_user)

    async def create(self, item):
        user = (await self.user_repo.filter(username=item.username)).first()
        if not user:
            raise AuthException().get_exception(1)

        is_logged = verify_password(item.password, user.password)
        if not is_logged:
            raise AuthException().get_exception(1)

        access_token_expires = timedelta(
            days=settings.ACCESS_TOKEN_EXPIRE_DAYS,
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        )
        token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )

        token = await self.repo.create(user_id=user.id, token=token)
        if not token:
            raise AuthException().get_exception(1)

        return TokenResponse(access_token=token.token, token_type="bearer")
