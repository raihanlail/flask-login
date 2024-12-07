from pydantic import BaseModel, constr
from typing import Annotated

class RatingsSchema:
    rating: Annotated[float, constr(ge=1, le=5)]
    