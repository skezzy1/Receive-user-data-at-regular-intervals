from common.pagination import CustomPage
from dependencies import UserDep
from fastapi import APIRouter
from users.schemas.users import UserListResponseSchema, UserResponseSchema

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "/",
    response_model=CustomPage[UserListResponseSchema],
    description="List users in database ",
)
def get_user_list(service: UserDep):
    return service.get_user_list()


@router.get("/{id}", response_model=UserResponseSchema)
def get_user(id: int, service: UserDep):
    return service.get_user_or_404(id)
