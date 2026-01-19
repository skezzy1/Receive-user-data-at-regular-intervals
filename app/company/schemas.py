from common.validations import IDValidation
from models import APIModel, ORMResponse
from pydantic import ConfigDict


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
