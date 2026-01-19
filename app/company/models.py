from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column
from db.base_model import BaseModel


class CompanyModel(BaseModel):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    catchPhrase: Mapped[str] = mapped_column(String(255), nullable=False)
    bs: Mapped[str] = mapped_column(String(255), nullable=False)

    users: Mapped[list["UserModel"]] = relationship("UserModel", back_populates="company")
