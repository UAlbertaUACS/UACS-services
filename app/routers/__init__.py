from fastapi import HTTPException, status
from app import main


async def check_admin_access(user: dict):
    """
    Check if user has admin access
    """
    mongoUser = await main.app.mongodb["users"].find_one({"email": user["email"]})
    if mongoUser is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    if "admin" not in mongoUser["roles"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    
