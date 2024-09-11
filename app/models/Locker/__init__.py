from pydantic import BaseModel, EmailStr, Field
from datetime import date
from typing import List, Optional

class Locker(BaseModel):
    id: str
    lockerNumber: int
    ownerEmail: EmailStr
    previousOwnerEmail: Optional[EmailStr]
    combination: str
    expiryDate: str
    newExpirationDate: date
    status: str
    notes: str
    year: int