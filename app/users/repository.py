from common.pagination import CustomPage
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.orm import Session
from users.models import UserModel
from users.schemas.users import UserListResponseSchema


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, user_id: int) -> UserModel | None:
        stmt = select(UserModel).where(UserModel.id == user_id)
        result = self.session.execute(stmt)
        return result.scalar_one_or_none()

    def get_by_external_id(self, external_id: int) -> UserModel | None:
        stmt = select(UserModel).where(UserModel.id == external_id)
        result = self.session.execute(stmt)
        return result.scalar_one_or_none()

    def get_user_list(self) -> CustomPage[UserListResponseSchema]:
        users = select(UserModel)
        return paginate(self.session, users)

    def add(self, user: UserModel) -> None:
        self.session.add(user)

    def update_from_api(self, user: UserModel, data: dict) -> None:
        user.name = data["name"]
        user.email = data["email"]
        user.username = data["username"]
