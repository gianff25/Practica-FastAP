from pydantic import ValidationError

from apps.users.models import UserDB
from apps.users.schemas.user import UserResponse, ValidUser
from utils.auth import hash_password
from utils.schemas import MessageResponse


class UserService:
    def create(item):
        user_data = ValidUser(
            username=item.username, email=item.email, is_staff=False, is_active=True
        )
        user_data.password = hash_password(item.password)
        user = UserDB().where(username=user_data.username, deleted=None).first()
        if user:
            raise ValidationError(msg="User already exists")
        UserDB().create(**user_data.dict())
        return MessageResponse(message="User created")
