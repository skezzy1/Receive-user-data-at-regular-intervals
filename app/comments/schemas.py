from typing import Annotated
from models import APIModel, ORMResponse
from pydantic import Field, EmailStr, ConfigDict
from pydantic.types import StrictStr

PostID = Annotated[int, Field(ge=1)]
CommentID = Annotated[int, Field(ge=1)]
LengthValidation = Annotated[
    StrictStr,
    Field(min_length=1, max_length=225, pattern=r"^[A-Za-z]+(?:[ '-]?[A-Za-z]+)*$"),
]


class CommentsPostBaseSchema(APIModel):
    postId: PostID
    id: CommentID
    name: LengthValidation
    email: EmailStr
    body: LengthValidation

    model_config = ConfigDict(
        json_schema_extra={
            "example": [
                {
                    "postId": 1,
                    "id": 1,
                    "name": "id labore ex et quam laborum",
                    "email": "Eliseo@gardner.biz",
                    "body": "laudantium enim quasi est quidem magnam voluptate ipsam eos\ntempora quo necessitatibus\ndolor quam autem quasi\nreiciendis et nam sapiente accusantium",
                }
            ]
        }
    )


class CommentsPostCreateSchema(CommentsPostBaseSchema):
    pass


class CommentsPostResponseSchema(ORMResponse):
    postId: int
    id: int
    email: EmailStr
    body: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": [
                {
                    "postId": 1,
                    "id": 1,
                    "name": "id labore ex et quam laborum",
                    "email": "Eliseo@gardner.biz",
                    "body": "laudantium enim quasi est quidem magnam voluptate ipsam eos\ntempora quo necessitatibus\ndolor quam autem quasi\nreiciendis et nam sapiente accusantium",
                }
            ]
        }
    )


class CommentsPostResponseListSchema(ORMResponse):
    postId: int
    id: int
    name: str
    email: EmailStr
    body: str

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "postId": 1,
                    "id": 1,
                    "name": "id labore ex et quam laborum",
                    "email": "Eliseo@gardner.biz",
                    "body": "laudantium enim quasi est quidem magnam voluptate ipsam eos\ntempora quo necessitatibus\ndolor quam autem quasi\nreiciendis et nam sapiente accusantium",
                },
                {
                    "postId": 1,
                    "id": 2,
                    "name": "quo vero reiciendis velit similique earum",
                    "email": "Jayne_Kuhic@sydney.com",
                    "body": "est natus enim nihil est dolore omnis voluptatem numquam\net omnis occaecati quod ullam at\nvoluptatem error expedita pariatur\nnihil sint nostrum voluptatem reiciendis et",
                },
                {
                    "postId": 1,
                    "id": 3,
                    "name": "odio adipisci rerum aut animi",
                    "email": "Nikita@garfield.biz",
                    "body": "quia molestiae reprehenderit quasi aspernatur\naut expedita occaecati aliquam eveniet laudantium\nomnis quibusdam delectus saepe quia accusamus maiores nam est\ncum et ducimus et vero voluptates excepturi deleniti ratione",
                },
            ]
        }
    )
