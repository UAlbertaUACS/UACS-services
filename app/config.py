import os
from typing import Annotated
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import pathlib


basedir = pathlib.Path(__file__).parents[1]
load_dotenv(basedir / ".env")

class Settings(BaseSettings):
    mongo_uri: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    root_path: str = ""
    env: str = os.getenv("ENV", "dev")
    logging_level: str = "INFO"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    frontend_url: str = os.getenv("FRONTEND_URL", "NA")

settings = Settings()