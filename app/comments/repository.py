from comments.models import CommentsModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class CommentsRepository:
    def __init__(self, session: AsyncSession):
        self.db = session

    async def get_comment_by_id(self, id: int) -> CommentsModel:
        query = select(CommentsModel).where(CommentsModel.id == id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
