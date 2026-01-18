from sqlalchemy.orm import Session
from sqlalchemy import select
from comments.models import CommentsModel
from fastapi_pagination.ext.sqlalchemy import paginate

from common.pagination import CustomPage

from comments.schemas import CommentsPostResponseListSchema


class CommentsRepository:
    def __init__(self, session: Session):
        self.db = session

    def get_comment_by_id(self, id: int) -> CommentsModel | None:
        query = select(CommentsModel).where(CommentsModel.id == id)
        result = self.db.execute(query)
        return result.scalar_one_or_none()

    def get_comments_list(self) -> CustomPage[CommentsPostResponseListSchema]:
        query = select(CommentsModel)
        return paginate(self.db, query)
