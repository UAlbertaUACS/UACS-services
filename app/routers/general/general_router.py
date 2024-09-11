from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.utils.auth import get_firebase_user_from_token
from app.models.Locker.methods import get_all_available_lockers, rent_locker
from app.models.Order import Order
from app.models.Order.methods import create_order
from app import main
import os

router = APIRouter()

@router.get("/healthcheck")
def health_check():
    # generate git commit version 
    git_sha = os.popen("git rev-parse HEAD").read().strip()
    return {"status": "ok", "git_sha": git_sha}