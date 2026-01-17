from db.base_model import BaseModel
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from users.models import UserModel


class PostModel(BaseModel):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    body: Mapped[str] = mapped_column(String(255), nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["UserModel"] = relationship("UserModel", back_populates="posts")

    comments: Mapped[list["CommentsModel"]] = relationship(
        "CommentsModel",
        back_populates="post",
        cascade="all, delete-orphan"
    )
