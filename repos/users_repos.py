from typing import List

from .base import BaseRepo
from models import  user_models
from core import security
from datetime import datetime
from database import user as users_db


class UserRepo(BaseRepo):
    async def create_user(self,u: user_models.User_input) -> user_models.User:
        user = user_models.User(
            id = 0,
            login = u.login,
            name = u.name,
            position = u.position,
            active = u.active,
            updated_at = datetime.utcnow(),
            password = security.to_hash_pass(u.password_first),
            created_at = datetime.utcnow()
        )
        user_values = {**user.dict()}
        user_values.pop('id',None)
        query = users_db.insert().values(user_values)
        user.id = await self.database.execute(query)
        return user

    async def read_users(self, skip: int =0, limit: int=100) -> List[user_models.User_base]:
        query = users_db.select().limit(limit).offset(skip)
        return await self.database.fetch_all(query)

    async def get_user_by_login(self, login) -> user_models.User:
        query = users_db.select().where(users_db.c.login == login)
        return await self.database.fetch_one(query)

    async def user_disable(self, login) -> user_models.User:
        query = users_db.update().where(users_db.c.login == login).values({'active': False, 'updated_at': datetime.utcnow()})
        await self.database.execute(query)
        return await self.get_user_by_login(login)

    async def user_enable(self, login) -> user_models.User:
        query = users_db.update().where(users_db.c.login == login).values({'active': True, 'updated_at': datetime.utcnow()})
        await self.database.execute(query)
        return await self.get_user_by_login(login)

