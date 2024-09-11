from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from enum import Enum
# import Optional
from typing import Optional
from bson.objectid import ObjectId


class Type(str, Enum):
    """
    Enum for Order types
    """
    locker = "locker"
    hoodie = "hoodie"
    room_access = "room_access"

class Status(str, Enum):
    """
    Enum for Order status
    """
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    cancelled = "cancelled"

class Order(BaseModel):
    """
    Order model
    """
    id: str
    type: Type
    user_email: EmailStr
    locker_id: Optional[int] = None
    hoodie_size: Optional[str] = None
    room_access: Optional[bool] = None
    expiry: Optional[str] = None
    year: Optional[int] = None
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[str] = None
    deleted_at: Optional[str] = None
    transaction_id: Optional[str] = None
    status: Optional[Status] = None
    reviewer_email: Optional[EmailStr] = None
    class Config:
        orm_mode = True