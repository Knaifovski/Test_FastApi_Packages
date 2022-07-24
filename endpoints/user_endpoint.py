from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from repos.users_repos import UserRepo
from .Depends import get_user_repos
from models import user_models


router = APIRouter()

@router.post('/',response_model=user_models.User)
async def create_user(user: user_models.User_input , users: UserRepo = Depends(get_user_repos)):
    if await users.get_user_by_login(user.login) != None:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail='User exist')
    return await users.create_user(user)

@router.get('/', response_model=List[user_models.User_base])
async def read_users(users_db: UserRepo = Depends(get_user_repos), skip: int =0, limit: int = 100):
    return await users_db.read_users(skip=skip, limit=limit)

@router.get('/id/', response_model=user_models.User_base)
async def get_user_by_login(users_db: UserRepo = Depends(get_user_repos), userlogin: str = ''):
    return await users_db.get_user_by_login(userlogin)

@router.patch('/disable', response_model=user_models.User)
async def to_disable_user(users_db: UserRepo = Depends(get_user_repos), userlogin: str=''):
    user = await users_db.get_user_by_login(userlogin)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    if user.active == False:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail='User already disabled')
    return await users_db.user_disable(userlogin)

@router.patch('/enable', response_model=user_models.User)
async def to_enable_user(users_db: UserRepo = Depends(get_user_repos), userlogin: str=''):
    user = await users_db.get_user_by_login(userlogin)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    if user.active == True:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail='User already enabled')
    return await users_db.user_enable(userlogin)