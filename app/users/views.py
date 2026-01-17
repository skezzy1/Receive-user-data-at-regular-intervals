from fastapi import APIRouter
from dependencies import UserDep
from users.schemas.users import UserListResponseSchema, UserResponseSchema
from fastapi_pagination import paginate
from users.schemas.users import CustomPage

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=CustomPage[UserListResponseSchema])
async def get_users(service: UserDep):
    users = await service.get_user_list_from_api()
    return paginate(users)


@router.get("/{id}", response_model=UserResponseSchema)
async def get_user(id: int, service: UserDep):
    return await service.get_user_by_id(id)


@router.post("/", response_model=list)
async def create_user(service: UserDep):
    return await service.fetch_and_save_users()
