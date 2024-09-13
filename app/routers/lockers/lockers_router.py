from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.utils.auth import get_firebase_user_from_token
from app.models.Locker.methods import get_all_available_lockers, rent_locker
from app.models.Order import Order
from app.models.Order.methods import create_order
from app.routers import check_admin_access
from app import main
# import uuid
import uuid

router = APIRouter()

# locker = await main.app.mongodb["lockers"].find_one({"lockerNumber": locker_id})

@router.get("/get-available-lockers")
async def get_available_lockers(user: dict = Depends(get_firebase_user_from_token)):
    """
    Get all available lockers
    """
    lockers = await get_all_available_lockers()
    return {"lockers": lockers}

@router.post("/order-rent-locker")
async def rent_locker(request:Request, user: dict = Depends(get_firebase_user_from_token)):
    """
    Create an order to rent a locker
    """
    # TODO: Add validation for expiry date
    # TODO: Add validation if the locker is already rented
    body = await request.json()
    locker_id = body.get("locker_id")
    expiry = body.get("expiry")
    year = body.get("year")
    transaction_id = body.get("transaction_id")
    if locker_id is None or expiry is None or year is None or transaction_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing parameters")
    # get body from request
    locker = await main.app.mongodb["lockers"].find_one({"lockerNumber": locker_id})
    if locker is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Locker not found")
    if locker["ownerEmail"] != "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Locker is not available")
    order = Order(
       id=str(uuid.uuid4()),
       type= "locker", user_email=user["email"], locker_id=locker_id, expiry=expiry, year=year, status="pending", transaction_id=transaction_id
        )
    return await create_order(order)

@router.get("/get-my-lockers")
async def get_my_locker(user: dict = Depends(get_firebase_user_from_token)):
    """
    Get the locker of the user
    """
    locker = await main.app.mongodb["lockers"].find({"ownerEmail": user["email"]}, {"_id": 0}).to_list(None)
    return {"lockers": locker}

# @router.post("/deallocate-locker")
# async def deallocate_locker(request: Request, user: dict = Depends(get_firebase_user_from_token)):
#     """
#     Deallocate a locker
#     """
#     body = await request.json()
#     locker_id = body.get("locker_id")
#     if locker_id is None:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing parameters")
#     locker = await main.app.mongodb["lockers"].find_one({"lockerNumber": locker_id})
#     if locker is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Locker not found")
#     if locker["ownerEmail"] != user["email"]:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You do not own this locker")
#     return await deallocate_locker(locker_id)

@router.get("/get-all-lockers")
async def get_all_lockers(user: dict = Depends(get_firebase_user_from_token)):
    """
    Get all lockers
    """
    error = await check_admin_access(user)
    if error:
        raise error
    lockers  = await main.app.mongodb["lockers"].find({}, {"_id": 0}).to_list(length=None)

    return {"lockers": lockers}