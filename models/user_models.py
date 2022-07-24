from pydantic import BaseModel, validator, constr
from typing import Optional

from datetime import datetime

class User_base(BaseModel):
    login: str
    name: str
    position: str
    active: bool = True
    updated_at: datetime

class User(User_base):
    id: Optional[int] = None
    password: str
    created_at: datetime

class User_input(User_base):
    password_first: constr(min_length=6, max_length=15)
    password_second: str

    @validator('password_second')
    def password_match(cls, v, values, **kwargs):
        if 'password_first' in values and v != values['password_first']:
            raise ValueError('passwords not match')
        return v