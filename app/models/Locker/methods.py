# from bson.objectid import ObjectId
from typing import List

from app.models.Locker import Locker
from app import main

async def get_locker_by_id(locker_id: int) -> Locker:
    """
    Get locker by id
    """
    locker = await main.app.mongodb["lockers"].find_one({"lockerNumber": locker_id})
    return None

async def get_all_available_lockers() -> List[Locker]:
    """
    Get all available lockers
    """
    pendingLockerOrders = await main.app.mongodb["orders"].find({"status": "pending", "type": "locker"}, {'_id': 0}).to_list(None)
    pendingLockerOrderLockerNumbers = [order["locker_id"] for order in pendingLockerOrders]
    lockers = await main.app.mongodb["lockers"].find({"ownerEmail": "", "lockerNumber": {"$nin": pendingLockerOrderLockerNumbers}}, {'_id': 0}).to_list(None)
    return lockers

async def rent_locker(locker_id: int, user_email: str, expiry: str, year: int) -> bool:
    """
    Book a locker
    """
    locker = await main.app.mongodb["lockers"].find_one({"lockerNumber": locker_id})
    if locker is None:
        return False
    if locker["ownerEmail"] != "":
        return False
    locker["ownerEmail"] = user_email
    locker["expiryDate"] = expiry
    locker["year"] = year
    await main.app.mongodb["lockers"].update_one({"lockerNumber": locker_id}, {"$set": locker})
    return True

async def get_all_lockers() -> List[Locker]:
    """
    Get all lockers
    """
    lockers = await main.app.mongodb["lockers"].find().to_list(None)
    return lockers

async def deallocate_locker(locker_id: int) -> bool:
    """
    Deallocate a locker
    """
    locker = await main.app.mongodb["lockers"].find_one({"lockerNumber": locker_id})
    if locker is None:
        return False
    previous_owner_email = locker["ownerEmail"]
    locker["previousOwnerEmail"] = previous_owner_email
    locker["ownerEmail"] = ""
    locker["expiryDate"] = ""
    locker["year"] = 0
    await main.app.mongodb["lockers"].update_one({"lockerNumber": locker_id}, {"$set": locker})
    return previous_owner_email

async def swap_locker_passcodes(locker_id: int, new_locker_id: int) -> bool:
    """
    Swap locks between two lockers
    """
    locker1 = await main.app.mongodb["lockers"].find_one({"lockerNumber": locker_id})
    locker2 = await main.app.mongodb["lockers"].find_one({"lockerNumber": new_locker_id})
    locker1.combination, locker2.combination = locker2.combination, locker1.combination

    await main.app.mongodb["lockers"].update_one({"lockerNumber": locker_id}, {"$set": locker1})
    await main.app.mongodb["lockers"].update_one({"lockerNumber": new_locker_id}, {"$set": locker2})

    return True