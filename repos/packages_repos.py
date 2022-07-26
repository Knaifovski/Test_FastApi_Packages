from typing import List

from datetime import datetime

from database.base import database
from database.package_table import package as package_db
from models import package_models
from .base import BaseRepo


class PackageRepo(BaseRepo):

    async def create_package(self, userid:int , p: package_models.Package):
        package = package_models.Package_In(
            id = 0,
            user_id = userid,
            weight = p.weight,
            comment = p.comment,
            created_at = datetime.utcnow(),
            updated_at = datetime.utcnow()
        )
        values = {**package.dict()}
        values.pop('id',None)
        query = package_db.insert().values(values)
        package.id = await database.execute(query)
        return package

    async def get_packages(self, limit: int = 100, skip: int = 0):
        query = package_db.select().limit(limit).offset(skip)
        return await database.fetch_all(query)

    async def get_client_packages(self, user_id: int, limit: int = 100, skip: int = 0):
        query = package_db.select().where(package_db.c.user_id == user_id).limit(limit).offset(skip)
        return await database.fetch_all(query)