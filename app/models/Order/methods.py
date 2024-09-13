from app.models.Order import Order
from app.models.Locker.methods import rent_locker
from app import main
from typing import List

async def get_order_by_id(order_id: str) -> Order:
    """
    Get order by id
    """
    order = await main.app.mongodb["orders"].find_one({"_id": order_id})
    return order

async def get_all_orders() -> List[Order]:
    """
    Get all orders
    """
    orders = await main.app.mongodb["orders"].find({}, {"_id":0}).to_list(None)
    return orders

async def get_all_pending_orders() -> List[Order]:
    """
    Get all pending orders
    """
    orders = await main.app.mongodb["orders"].find({"status": "pending"}, {"_id": 0, "id": 1, "type": 1, "user_email": 1, "locker_id": 1, "transaction_id": 1, "status": 1, "expiry": 1, "year": 1, "created_at": 1}).to_list(None)
    return orders

async def create_order(order: Order) -> bool:
    """
    Create an order
    """
    await main.app.mongodb["orders"].insert_one(order.dict())
    return True

async def approve_order(order_id: str, reviewer_email:str) -> bool:
    """
    Approve an order
    """
    order = await main.app.mongodb["orders"].find_one({"id": order_id})
    # print(order)
    if order is None:
        return False, False
    order["status"] = "approved"
    order["reviewer_email"] = reviewer_email
    locker = await main.app.mongodb["lockers"].find_one({"lockerNumber": order["locker_id"]})
    if locker is None:
        return False, False
    locker["ownerEmail"] = order["user_email"]
    locker["expiryDate"] = order["expiry"]
    locker["year"] = order["year"]
    await main.app.mongodb["lockers"].update_one({"lockerNumber": order["locker_id"]}, {"$set": locker})

    await main.app.mongodb["orders"].update_one({"id": order_id}, {"$set": order})

    if order["type"] == "locker":
        await rent_locker(order["locker_id"], order["user_email"], order["expiry"], order["year"])
    return order["user_email"], locker

async def reject_order(order_id: str, reviewer_email: str) -> bool:
    """
    Reject an order
    """
    order = await main.app.mongodb["orders"].find_one({"id": order_id})
    if order is None:
        return False
    order["status"] = "rejected"
    order["reviewer_email"] = reviewer_email
    await main.app.mongodb["orders"].update_one({"id": order_id}, {"$set": order})
    return order["user_email"]