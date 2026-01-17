from models import APIModel, ORMResponse
from typing import Annotated
from pydantic import ConfigDict, Field
from pydantic.types import StrictStr
from common.validations import IDValidation

from users.schemas.geo import GeoBaseSchema

LengthValidation = Annotated[
    StrictStr,
    Field(min_length=1, max_length=225, pattern=r"^[A-Za-z]+(?:[ '-]?[A-Za-z]+)*$"),
]


class AddressBaseSchema(APIModel):
    id: IDValidation
    street: LengthValidation
    suite: LengthValidation
    city: LengthValidation
    zipcode: str
    geo: GeoBaseSchema

    model_config = ConfigDict(
        json_schema_extra={
            "example": [
                {
                    "id": 1,
                    "street": "Victor Plains",
                    "suite": "Suite 879",
                    "city": "Wisokyburgh",
                    "zipcode": "90566-7771",
                    "geo": {"lat": "-43.9509", "lng": "-34.4618"},
                }
            ]
        }
    )


class AddressResponseSchema(ORMResponse):
    id: int
    street: str
    suite: str
    city: str
    zipcode: str
    geo: GeoBaseSchema

    model_config = ConfigDict(
        json_schema_extra={
            "example": [
                {
                    "id": 1,
                    "street": "Victor Plains",
                    "suite": "Suite 879",
                    "city": "Wisokyburgh",
                    "zipcode": "90566-7771",
                    "geo": {"lat": "-43.9509", "lng": "-34.4618"},
                }
            ]
        }
    )


class AddressListResponseSchema(ORMResponse):
    id: int
    street: str
    suite: str
    city: str
    zipcode: str
    geo: dict

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "id": 1,
                    "street": "Kulas Light",
                    "suite": "Apt. 556",
                    "city": "Gwenborough",
                    "zipcode": "92998-3874",
                    "geo": {"lat": "-37.3159", "lng": "81.1496"},
                },
                {
                    "id": 2,
                    "street": "Douglas Extension",
                    "suite": "Suite 847",
                    "city": "McKenziehaven",
                    "zipcode": "59590-4157",
                    "geo": {"lat": "-68.6102", "lng": "-47.0653"},
                },
            ]
        }
    )
