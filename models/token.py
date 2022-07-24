from pydantic import BaseModel


class Token(BaseModel):
    token: str
    type: str

class token_auth(BaseModel):
    login: str
    password: str