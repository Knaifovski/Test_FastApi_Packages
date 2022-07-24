from jose import jwt
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext

from datetime import datetime,timedelta

from .config import Setting

crypt = CryptContext(schemes=['bcrypt'], deprecated='auto')
settings = Setting()

def to_hash_pass(password: str) -> str:
    return crypt.hash(password)

def to_verify_pass(hash: str, password: str) ->bool:
    return crypt.verify(password, hash)

def create_access_token(data: dict) -> str:
    to_encode=data.copy()
    to_encode.update({'exp': datetime.utcnow() + timedelta(hours=settings.ACCESS_TOKEN_EXPIRED)})
    return jwt.encode(to_encode,settings.SECRET_KEY,settings.ALGHORITHM)

def decode_access_token(token: str):
    try:
        encoded_jwt=jwt.decode(token,settings.SECRET_KEY,settings.ALGHORITHM)
    except jwt.JWSError:
        return None
    return encoded_jwt


class JWTBearer(HTTPBearer):

    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        if credentials:
            token = decode_access_token(credentials.credentials)
            if token is None:
                raise exception
            return credentials.credentials
        else:
            return exception