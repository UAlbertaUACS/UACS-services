from pydantic import BaseModel, EmailStr, Field
from enum import Enum
from typing import List, Optional

class Role(str, Enum):
    """
    Enum for User roles
    """
    admin = "admin"
    user = "user"
    mod = "mod"


class User(BaseModel):
    """
    User model
    """
    email: EmailStr
    name: str
    roles: List[Role]

    class Config:
        orm_mode = True