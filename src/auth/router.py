from fastapi import APIRouter

from src.auth.auth import auth_backend
from src.auth.schemas import UserRead, UserCreate, UserUpdate
from src.auth.auth import fastapi_users

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)
router.include_router(fastapi_users.get_auth_router(auth_backend))
router.include_router(fastapi_users.get_register_router(UserRead, UserCreate))
# router.include_router(
#     fastapi_users.get_users_router(UserRead, UserUpdate),
#     prefix="/users",
# )