from common.pagination import CustomPage
from dependencies import PostDep
from fastapi import APIRouter
from fastapi_pagination import paginate
from posts.schemas import PostListResponseSchema, PostResponseSchema

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", response_model=CustomPage[PostListResponseSchema])
async def fetch_posts_from_api(service: PostDep):
    posts = await service.fetch_posts_from_api()
    return paginate(posts)


@router.get("/list", response_model=CustomPage[PostListResponseSchema])
async def get_posts(service: PostDep, payload: PostListResponseSchema):
    posts = await service.get_posts_list(payload)
    return paginate(posts)


@router.get("/{id}", response_model=PostResponseSchema)
async def get_post(service: PostDep, id: int):
    return await service.get_post_or_404(id)
