from sqlalchemy.orm import Session
from sqlalchemy import select
from posts.models import PostModel
from common.pagination import CustomPage
from posts.schemas import PostListResponseSchema
from fastapi_pagination.ext.sqlalchemy import paginate


class PostsRepository:
    def __init__(self, session: Session):
        self.db = session

    def get_post_by_id(self, id: int) -> PostModel | None:
        query = select(PostModel).where(PostModel.id == id)
        result = self.db.execute(query)
        return result.scalar_one_or_none()

    def get_posts_list(self) -> CustomPage[PostListResponseSchema]:
        query = select(PostModel)
        return paginate(self.db, query)
