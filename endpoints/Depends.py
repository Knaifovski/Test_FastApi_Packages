from fastapi import Depends, HTTPException, status

from core.security import JWTBearer, decode_access_token
from models import user_models
from repos.users_repos import UserRepo
from repos.packages_repos import PackageRepo
from database.base import database

def get_user_repos() -> UserRepo:
    return UserRepo(database)

def get_package_repos() -> PackageRepo:
    return PackageRepo(database)

async def get_current_user(
        user: UserRepo = Depends(get_user_repos),
        token: str = Depends(JWTBearer())
    ) -> user_models.User:
    cred_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='NOT VALID')
    payload = decode_access_token(token)
    if payload is None:
        raise cred_exception
    login: str = payload.get('sub')
    if login is None:
        raise cred_exception
    user = await user.get_user_by_login(login = login)
    if user is None:
        raise cred_exception
    return user