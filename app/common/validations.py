from typing import Annotated

from pydantic import Field, StrictStr

IDValidation = Annotated[int, Field(ge=1)]

LengthValidation = Annotated[
    StrictStr,
    Field(min_length=1, max_length=225, pattern=r"^[A-Za-z]+(?:[ '-]?[A-Za-z]+)*$"),
]
