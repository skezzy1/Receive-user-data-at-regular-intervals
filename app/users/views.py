from common.pagination import CustomPage
from dependencies import UserDep
from fastapi import APIRouter
from fastapi_pagination import paginate
from users.schemas.users import UserListResponseSchema, UserResponseSchema

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "/",
    response_model=CustomPage[UserListResponseSchema],
    description="List users by API",
)
async def get_users(service: UserDep):
    users = await service.fetch_users_from_api()
    return paginate(users)


@router.get(
    "/list",
    response_model=CustomPage[UserListResponseSchema],
    description="List users in database ",
)
async def get_user_list(service: UserDep, payload: UserListResponseSchema):
    users = await service.get_user_list(payload)
    return paginate(users)


@router.get("/{id}", response_model=UserResponseSchema)
async def get_user(id: int, service: UserDep):
    return await service.get_user_or_404(id)
