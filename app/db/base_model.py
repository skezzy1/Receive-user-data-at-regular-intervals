from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase


class BaseModel(DeclarativeBase):
    @classmethod
    def default_order_by(cls) -> list | None:
        """
        This method returns list of rows for default ordering.

        This method preferably should be overridden by subclasses.
        Use this method when set up ordering. Example:
        `select(SubModel).order_by(*SubModel.default_order_by())`

        :return: list of ordering rows
        """
        return None

    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_`%(constraint_name)s`",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )
