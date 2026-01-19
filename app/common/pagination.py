from typing import TypeVar

from fastapi import Query
from fastapi_pagination import Page
from fastapi_pagination.customization import CustomizedPage, UseParamsFields

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
