from typing import Annotated
from pydantic import Field

IDValidation = Annotated[int, Field(ge=1)]
