from fastapi import APIRouter

from apps.auth.routers import auth_router
from apps.placeholder.routers import dummy_router
from apps.users.routers import user_router

api_router = APIRouter()
api_router.include_router(dummy_router, tags=["Dummies"], prefix="/dummies")
api_router.include_router(user_router, tags=["Users"], prefix="/users")
api_router.include_router(auth_router, tags=["Auth"], prefix="/auth")

# For health-checking purposes
api_router.add_api_route(
    "/", endpoint=lambda: {"message": "Service is up"}, methods=["GET"], tags=["Service"]
)
