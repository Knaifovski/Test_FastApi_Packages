from typing import Optional

from pydantic import BaseModel

from datetime import datetime


class Package(BaseModel):
    id: Optional[int] = None
    user_id: int
    weight: float
    comment: str
    updated_at: datetime


class Package_out(Package):
    pass


class Package_In(Package):
    created_at: datetime