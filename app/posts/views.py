from common.pagination import CustomPage
from dependencies import PostDep
from fastapi import APIRouter
from posts.schemas import PostListResponseSchema, PostResponseSchema

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", response_model=CustomPage[PostListResponseSchema])
def get_posts(service: PostDep):
    return service.get_posts_list()


@router.get("/{id}", response_model=PostResponseSchema)
def get_post(service: PostDep, id: int):
    return service.get_post_or_404(id)
