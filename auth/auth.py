from fastapi_users import FastAPIUsers
from fastapi_users.authentication import CookieTransport, JWTStrategy, AuthenticationBackend
from .models import User
from .manager import get_user_manager

cookie_transport = CookieTransport(cookie_name="custom_name", cookie_max_age=30*24*60*60)

SECRET = "SECRET"


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=30*24*60*60)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()
