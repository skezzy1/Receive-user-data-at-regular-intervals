from typing import Annotated, Callable, Type, TypeVar

from fastapi import Depends
from sqlalchemy.orm import Session

from db.session_postgresql import get_postgresql_db

from comments.services import CommentsService
from comments.repository import CommentsRepository
from posts.repository import PostsRepository
from posts.services import PostsService
from users.repository import UserRepository
from users.services import UserService

S = TypeVar("S")
R = TypeVar("R")


def service(cls: Type[S], repo_cls: Type[R]) -> Callable[[Session], S]:
    def _dep(db: Session = Depends(get_postgresql_db)) -> S:
        repo = repo_cls(db)
        return cls(repo)

    return _dep


# Aliases
UserDep = Annotated[UserService, Depends(service(UserService, UserRepository))]
PostDep = Annotated[PostsService, Depends(service(PostsService, PostsRepository))]
CommentsDep = Annotated[CommentsService, Depends(service(CommentsService, CommentsRepository))]
