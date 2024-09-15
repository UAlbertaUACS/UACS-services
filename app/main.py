import time
from typing import Any, Callable, TypeVar
import uvicorn
from fastapi import FastAPI, Request, Response
from app.config import settings
from app.routers.lockers import lockers_router
from app.routers.orders import orders_router
from app.routers.general import general_router
import firebase_admin
import pathlib
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from app.utils.db import lifespan

basedir = pathlib.Path(__file__).parents[1]
load_dotenv(basedir / ".env")

app = FastAPI(
    title="Backend UACS",
    description="",
    version="1.0.0",
    docs_url=None,
    root_path=settings.root_path,
    lifespan=lifespan,
)
origins = settings.frontend_urls
# print(f"Allowed origins: {origins}")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(lockers_router.router, prefix="/lockers")
app.include_router(orders_router.router, prefix="/orders")
app.include_router(general_router.router, prefix="/v1")

firebase_admin.initialize_app()

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        log_level="debug",
        reload=True,
    )