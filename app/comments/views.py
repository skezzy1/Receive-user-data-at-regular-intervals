from common.pagination import CustomPage
from dependencies import CommentsDep
from fastapi import APIRouter
from fastapi_pagination import paginate
from comments.schemas import CommentsPostResponseListSchema, CommentsPostResponseSchema

router = APIRouter(prefix="/comments", tags=["comments"])


@router.get("/", response_model=CustomPage[CommentsPostResponseListSchema])
async def fetch_comments_from_api(service: CommentsDep):
    posts = await service.fetch_comments_from_api()
    return paginate(posts)


"""
@router.get("/list", response_model=CustomPage[CommentsPostResponseListSchema])
async def get_comments(service: CommentsDep):
    posts = await service.get_co()
    return paginate(posts)
"""


@router.get("/{id}", response_model=CommentsPostResponseSchema)
async def get_comment(service: CommentsDep, id: int):
    return await service.get_comments_or_404(id)
