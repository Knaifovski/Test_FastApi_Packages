from typing import List

from fastapi import APIRouter, Depends

from endpoints.Depends import get_package_repos, get_current_user
from models.package_models import Package
from repos import packages_repos
from repos.packages_repos import PackageRepo
from repos.users_repos import UserRepo

router = APIRouter()


@router.post('/', response_model=Package)
async def create_package(
        p: Package,
        current_user: UserRepo = Depends(get_current_user),
        package_db: PackageRepo = Depends(get_package_repos),
    ):
    return await package_db.create_package(userid = current_user.id, p = p )

@router.get('/', response_model = List[Package])
async def get_packages(skip: int = 0, limit: int = 100, package_db: PackageRepo = Depends(get_package_repos)):
    return await package_db.get_packages(skip=skip, limit=limit)

@router.get('/client', response_model= List[Package])
async def get_user_packages(skip: int = 0, limit: int = 100,
                            packages_db: PackageRepo = Depends(get_package_repos),
                            current_user: UserRepo = Depends(get_current_user)
                            ):
    return await packages_db.get_client_packages(user_id=current_user.id, skip=skip, limit=limit)