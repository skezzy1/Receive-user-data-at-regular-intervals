from typing import TypeVar, Type, Callable, Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from users.services import UserService
from users.repository import UserRepository
from db.session_postgresql import get_postgresql_db

S = TypeVar("S")
R = TypeVar("R")

def service(cls: Type[S], repo_cls: Type[R]) -> Callable[[AsyncSession], S]:
    def _dep(db: AsyncSession = Depends(get_postgresql_db)) -> S:
        repo = repo_cls(db)
        return cls(db, repo)
    return _dep

# Aliases
UserDep = Annotated[UserService, Depends(service(UserService, UserRepository))]