from pydantic import BaseModel, EmailStr, constr
from typing import Annotated

class EditProfileSchema(BaseModel):
    username: Annotated[str, constr(min_length=3, max_length=20, pattern=r'^[A-Za-z0-9_]+')]
    email: EmailStr
   