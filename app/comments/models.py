from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column
from db.base_model import BaseModel


class CommentsModel(BaseModel):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    body: Mapped[str] = mapped_column(String(1025), nullable=False)

    post_id: Mapped[int] = mapped_column("postId", ForeignKey("posts.id"), nullable=False)
    post: Mapped["PostModel"] = relationship("PostModel", back_populates="comments")
