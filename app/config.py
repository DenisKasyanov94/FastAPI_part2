from pydantic_settings import BaseSettings
from pydantic import Field


class Settings:
    secret_key = "your-super-secret-key-here-123"
    database_url = "sqlite:///./advertisements.db"

settings = Settings()