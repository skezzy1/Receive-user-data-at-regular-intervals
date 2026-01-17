from typing import Optional

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from users.views import router as user_router

class ErrorResponse(BaseModel):
    errors: Optional[list[str]]


api_router = APIRouter(
    default_response_class=JSONResponse,
    responses={
        400: {
            'model': ErrorResponse
        },
        401: {
            'model': ErrorResponse
        },
        403: {
            'model': ErrorResponse
        },
        404: {
            'model': ErrorResponse
        },
        500: {
            'model': ErrorResponse
        },
    },
)

api_router.include_router(user_router)

