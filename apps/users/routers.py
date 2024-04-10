from typing import List

from fastapi import APIRouter, Depends

from apps.users.schemas.user import UserRequest, UserResponse
from apps.users.services.user import UserService
from dependencies.database import get_db
from utils.schemas import MessageResponse

user_router = APIRouter()


@user_router.get("/{id}", response_model=UserResponse)
async def get_by_id(self, id: int, db: get_db = Depends()):
    return UserService.get(id)


@user_router.get("/", response_model=List[UserResponse])
async def get_all(self, db: get_db = Depends()):
    return UserService.get_all()


@user_router.post("/", response_model=MessageResponse)
async def create(self, item: UserRequest, db: get_db = Depends()):
    return UserService.create(item)
