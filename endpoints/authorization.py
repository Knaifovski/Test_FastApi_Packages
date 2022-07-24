from fastapi import APIRouter, Depends, HTTPException, status

from core.security import to_verify_pass, create_access_token
from models.token import token_auth, Token
from repos.users_repos import UserRepo
from endpoints.Depends import get_user_repos

router = APIRouter()

@router.post('/', response_model=Token)
async def login(auth: token_auth, users_db: UserRepo = Depends(get_user_repos)):
    user = await users_db.get_user_by_login(auth.login)
    if user is None or not to_verify_pass(password=auth.password, hash=user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not found or password error")

    return Token(
        token=create_access_token({'sub': user.login}),
        type="Bearer"
    )