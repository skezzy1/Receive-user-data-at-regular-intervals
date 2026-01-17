from models import APIModel
from pydantic import ConfigDict

from models import ORMResponse
from common.validations import IDValidation


class GeoBaseSchema(APIModel):
    id: IDValidation
    lat: float
    lng: float

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "id": 1,
                    "lat": "37.5",
                    "lng": "-79.4",
                }
            ]
        }
    )


class GeoResponseSchema(ORMResponse):
    id: int
    lat: float
    lng: float

    model_config = ConfigDict(
        json_schema_extra={
            "example": [
                {
                    "id": 1,
                    "lat": "37.5",
                    "lng": "-79.4",
                },
            ]
        }
    )


class GeoListResponseSchema(ORMResponse):
    id: IDValidation
    lat: float
    lng: float

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "id": 1,
                    "lat": "37.5",
                    "lng": "-79.4",
                },
                {
                    "id": 2,
                    "lat": "-354.5",
                    "lng": "79.4",
                },
            ]
        }
    )
