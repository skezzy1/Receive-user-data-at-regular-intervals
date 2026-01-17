from company.models import CompanyModel
from db.base_model import BaseModel
from sqlalchemy import Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship


class UserModel(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    username: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str] = mapped_column(String(255), nullable=False)
    website: Mapped[str] = mapped_column(String(255), nullable=False)

    address_id: Mapped[int] = mapped_column(ForeignKey("address.id"))
    address: Mapped["AddressModel"] = relationship(
        "AddressModel", back_populates="user", uselist=False
    )

    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"))
    company: Mapped["CompanyModel"] = relationship(
        "CompanyModel", back_populates="users", uselist=False
    )

    posts: Mapped[list["PostModel"]] = relationship("PostModel", back_populates="user")

    comments: Mapped[list["CommentsModel"]] = relationship("CommentsModel", back_populates="user")


class AddressModel(BaseModel):
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    street: Mapped[str] = mapped_column(String(255), nullable=False)
    suite: Mapped[str] = mapped_column(String(255), nullable=False)
    city: Mapped[str] = mapped_column(String(255), nullable=False)
    zipcode: Mapped[str] = mapped_column(String(255), nullable=False)

    geo_id: Mapped[int] = mapped_column(ForeignKey("geo.id"))
    geo: Mapped["GeoModel"] = relationship(
        "GeoModel", back_populates="address", uselist=False
    )

    user: Mapped["UserModel"] = relationship(
        "UserModel", back_populates="address", uselist=False
    )


class GeoModel(BaseModel):
    __tablename__ = "geo"
    __table_args__ = (UniqueConstraint("lat", "lng", name="uq_geo_lat_lng"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lat: Mapped[float] = mapped_column(Float, nullable=False)
    lng: Mapped[float] = mapped_column(Float, nullable=False)

    address: Mapped["AddressModel"] = relationship(
        "AddressModel", back_populates="geo", uselist=False
    )
