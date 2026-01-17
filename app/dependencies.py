from typing import Annotated, Callable, Type, TypeVar

from comments.services import CommentsService
from db.session_postgresql import get_postgresql_db
from fastapi import Depends
from posts.repository import PostsRepository
from posts.services import PostsService
from sqlalchemy.ext.asyncio import AsyncSession
from users.repository import UserRepository
from users.services import UserService
from comments.repository import CommentsRepository

S = TypeVar("S")
R = TypeVar("R")


def service(cls: Type[S], repo_cls: Type[R]) -> Callable[[AsyncSession], S]:
    def _dep(db: AsyncSession = Depends(get_postgresql_db)) -> S:
        repo = repo_cls(db)
        return cls(repo)

    return _dep


# Aliases
UserDep = Annotated[UserService, Depends(service(UserService, UserRepository))]
PostDep = Annotated[PostsService, Depends(service(PostsService, PostsRepository))]
CommentsDep = Annotated[CommentsService, Depends(service(CommentsService, CommentsRepository))]
