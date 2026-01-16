from typing import Optional, Annotated
from pydantic import BaseModel, Field, ConfigDict, field_validator, conint
from pydantic.types import StrictStr


class APIModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",            # reject unknown fields
        populate_by_name=True,     # allow aliases if you add them later
        str_strip_whitespace=True, # auto-trim strings
    )

class ORMResponse(APIModel):
    model_config = APIModel.model_config | ConfigDict(from_attributes=True)