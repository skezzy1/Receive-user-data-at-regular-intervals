from common.validations import IDValidation
from models import APIModel, ORMResponse
from pydantic import ConfigDict, Field


class PostBaseSchema(APIModel):
    user_id: IDValidation = Field(serialization_alias="userId")
    id: IDValidation
    title: str
    body: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"userId": 1, "id": 1, "title": "title", "body": "body"}
        }
    )


class PostCreateSchema(PostBaseSchema):
    pass


class PostResponseSchema(APIModel):
    user_id: IDValidation = Field(serialization_alias="userId")
    id: IDValidation
    title: str
    body: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"userId": 1, "id": 1, "title": "title", "body": "body"}
        }
    )


class PostListResponseSchema(ORMResponse):
    user_id: IDValidation = Field(serialization_alias="userId")
    id: IDValidation
    title: str
    body: str

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {"userId": 1, "id": 1, "title": "title", "body": "body"},
                {"userId": 2, "id": 2, "title": "title", "body": "body"},
            ]
        }
    )
