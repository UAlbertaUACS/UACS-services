from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from app.utils.auth import get_firebase_user_from_token
# from app.models.Locker.methods import get_all_available_lockers, rent_locker
from app.models.Order import Order
from app.models.Order.methods import create_order
from app import main
from app.models.Order.methods import get_all_orders, approve_order, reject_order, get_all_pending_orders
from app.routers import check_admin_access
from app.mail import send_email
from app.utils.utils import create_approved_locker_email, create_rejected_locker_email
from fastapi.requests import Request 

router = APIRouter()

@router.get("/get-all-orders")
async def get_all_orders_route(user: dict = Depends(get_firebase_user_from_token)):
    """
    Get all orders
    """
    error = await check_admin_access(user)
    if error:
        raise error
    orders = await get_all_orders()
    return {"orders": orders}

@router.get("/get-all-pending-orders")
async def get_all_pending_orders_route(user: dict = Depends(get_firebase_user_from_token)):
    """
    Get all pending orders
    """
    error = await check_admin_access(user)
    if error:
        raise error
    orders = await get_all_pending_orders()
    return {"orders": orders}

@router.post("/approve-order")
async def approve_order_route(order_id: str, user: dict = Depends(get_firebase_user_from_token)):
    """
    Approve an order
    """
    error = await check_admin_access(user)
    if error:
        raise error
    order_approved_email, locker = await approve_order(order_id, user["email"])
    if not order_approved_email:
        # Bad request
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Order invalid")
    send_email(create_approved_locker_email(name=user["name"], locker_number=locker["lockerNumber"], combination=locker["combination"]), order_approved_email, "CSC Locker Rental", "Lockers")
    return order_approved_email

@router.post("/reject-order")
async def reject_order_route(order_id: str, email:bool, request: Request, user: dict = Depends(get_firebase_user_from_token)):
    """
    Reject an order
    """
    error = await check_admin_access(user)
    if error:
        raise error
    order_rejected_email = await reject_order(order_id, user)
    if not order_rejected_email:
        # Bad request
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Order invalid")
    if email:
        body = await request.json()
        note = body["note"]
        if not note:
            note = "No reason provided. Contact execs@uacs.ca"
        send_email(create_rejected_locker_email(name=user["name"], notes=note), order_rejected_email, "CSC Locker Rental", "Lockers")
    return True

@router.get("/get-my-orders")
async def get_my_orders(user: dict = Depends(get_firebase_user_from_token)):
    """
    Get all orders of the user
    """
    orders = await main.app.mongodb["orders"].find({"user_email": user["email"]}, {"_id":0}).to_list(None)
    return {"orders": orders}