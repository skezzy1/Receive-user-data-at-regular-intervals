from typing import TypeVar

from fastapi import Query
from fastapi_pagination import Page
from fastapi_pagination.customization import CustomizedPage, UseParamsFields
from pydantic import ConfigDict, EmailStr

from models import APIModel, ORMResponse
from common.validations import IDValidation

from users.schemas.address import AddressBaseSchema
from company.schemas import CompanyBaseSchema


T = TypeVar("T")

CustomPage = CustomizedPage[
    Page[T],
    UseParamsFields(
        size=Query(
            10,
            ge=1,
            le=10,
            description="Items per page (limitation: from 1 to 10 objects per page)",
        ),
        page=Query(1, ge=1, description="Page number starts from 1"),
    ),
]


class UserBaseSchema(APIModel):
    id: IDValidation
    name: str
    username: str
    email: EmailStr
    address: AddressBaseSchema
    phone: str
    website: str
    company: CompanyBaseSchema


class CreateUserBaseSchema(UserBaseSchema):
    pass


class UserResponseSchema(ORMResponse):
    id: IDValidation
    name: str
    username: str
    email: EmailStr
    address: dict
    phone: str
    website: str
    company: dict

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "id": 1,
                    "name": "Leanne Graham",
                    "username": "Bret",
                    "email": "Sincere@april.biz",
                    "address": {
                        "street": "Kulas Light",
                        "suite": "Apt. 556",
                        "city": "Gwenborough",
                        "zipcode": "92998-3874",
                        "geo": {"lat": "-37.3159", "lng": "81.1496"},
                    },
                    "phone": "1-770-736-8031 x56442",
                    "website": "hildegard.org",
                    "company": {
                        "name": "Romaguera-Crona",
                        "catchPhrase": "Multi-layered client-server neural-net",
                        "bs": "harness real-time e-markets",
                    },
                }
            ]
        }
    )


class UserListResponseSchema(ORMResponse):
    id: int
    name: str
    username: str
    email: EmailStr
    address: dict
    phone: str
    website: str
    company: dict

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "id": 1,
                    "name": "Leanne Graham",
                    "username": "Bret",
                    "email": "Sincere@april.biz",
                    "address": {
                        "street": "Kulas Light",
                        "suite": "Apt. 556",
                        "city": "Gwenborough",
                        "zipcode": "92998-3874",
                        "geo": {"lat": "-37.3159", "lng": "81.1496"},
                    },
                    "phone": "1-770-736-8031 x56442",
                    "website": "hildegard.org",
                    "company": {
                        "name": "Romaguera-Crona",
                        "catchPhrase": "Multi-layered client-server neural-net",
                        "bs": "harness real-time e-markets",
                    },
                },
                {
                    "id": 2,
                    "name": "Ervin Howell",
                    "username": "Antonette",
                    "email": "Shanna@melissa.tv",
                    "address": {
                        "street": "Victor Plains",
                        "suite": "Suite 879",
                        "city": "Wisokyburgh",
                        "zipcode": "90566-7771",
                        "geo": {"lat": "-43.9509", "lng": "-34.4618"},
                    },
                    "phone": "010-692-6593 x09125",
                    "website": "anastasia.net",
                    "company": {
                        "name": "Deckow-Crist",
                        "catchPhrase": "Proactive didactic contingency",
                        "bs": "synergize scalable supply-chains",
                    },
                },
            ]
        }
    )
