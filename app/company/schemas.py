from models import APIModel, ORMResponse
from typing import Annotated
from pydantic import Field, ConfigDict
from pydantic.types import StrictStr
from common.validations import IDValidation

LengthValidation = Annotated[
    StrictStr,
    Field(min_length=1, max_length=225, pattern=r"^[A-Za-z]+(?:[ '-]?[A-Za-z]+)*$"),
]


class CompanyBaseSchema(APIModel):
    id: IDValidation
    name: str
    catchPhrase: str
    bs: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": [
                {
                    "id": 1,
                    "name": "Romaguera-Crona",
                    "catchPhrase": "Multi-layered client-server neural-net",
                    "bs": "harness real-time e-markets",
                }
            ]
        }
    )


class CompanyResponseSchema(ORMResponse):
    id: int
    name: str
    catchPhrase: str
    bs: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": [
                {
                    "id": 1,
                    "name": "Romaguera-Crona",
                    "catchPhrase": "Multi-layered client-server neural-net",
                    "bs": "harness real-time e-markets",
                }
            ]
        }
    )


class CompanyListResponseSchema(ORMResponse):
    id: int
    name: str
    catchPhrase: str
    bs: str

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "id": 1,
                    "name": "Romaguera-Crona",
                    "catchPhrase": "Multi-layered client-server neural-net",
                    "bs": "harness real-time e-markets",
                },
                {
                    "id": 2,
                    "name": "Deckow-Crist",
                    "catchPhrase": "Proactive didactic contingency",
                    "bs": "synergize scalable supply-chains",
                },
            ]
        }
    )
