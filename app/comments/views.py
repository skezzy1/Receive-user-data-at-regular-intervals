from common.pagination import CustomPage
from dependencies import CommentsDep
from fastapi import APIRouter
from comments.schemas import CommentsPostResponseListSchema, CommentsPostResponseSchema

router = APIRouter(prefix="/comments", tags=["comments"])


@router.get("/", response_model=CustomPage[CommentsPostResponseListSchema])
def get_comments(service: CommentsDep):
    return service.get_comments_list()


@router.get("/{id}", response_model=CommentsPostResponseSchema)
def get_comment(service: CommentsDep, id: int):
    return service.get_comments_or_404(id)
