from pydantic import BaseSettings

class Settings(BaseSettings):
    secret_key: str = "your-secret-key-change-in-production"
    database_url: str = "sqlite:///./advertisements.db"

    class Config:
        env_file = ".env"

settings = Settings()