from models import APIModel
from common.validations import IDValidation


class PostBaseSchema(APIModel):
    userId: IDValidation
    id: IDValidation
    title: str
    body: str
