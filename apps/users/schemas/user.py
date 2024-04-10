from typing import Optional

from utils.schemas import InclusiveModel, StrictModel


class Credential(StrictModel):
    username: str
    password: str


class UserRequest(StrictModel):
    username: str
    password: str
    email: str


class UserResponse(InclusiveModel):
    id: int
    username: str
    email: str
    created_by_id: str


class ValidUser(StrictModel):
    username: str
    password: Optional[str]
    email: Optional[str]
    is_staff: bool
    is_active: bool
