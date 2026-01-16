from typing import TypeVar, Type, Callable, Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.db.session_postgresql import get_postgresql_db


S = TypeVar("S")


def service(cls: Type[S]) -> Callable[[AsyncSession], S]:
    def _dep(db: AsyncSession = Depends(get_postgresql_db)) -> S:
        settings = get_settings()
        return cls(db)

    return _dep


# Aliases
#UserDep = Annotated[UserService, Depends(service(UserService))]