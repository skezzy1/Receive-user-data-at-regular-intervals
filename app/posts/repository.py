from posts.models import PostModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from common.pagination import CustomPage
from posts.schemas import PostListResponseSchema
from fastapi_pagination.ext.sqlalchemy import paginate


class PostsRepository:
    def __init__(self, session: AsyncSession):
        self.db = session

    async def get_post_by_id(self, id: int) -> PostModel:
        query = select(PostModel).where(PostModel.id == id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_posts_list(self) -> CustomPage[PostListResponseSchema]:
        users = select(PostModel)
        return await paginate(self.session, users)
