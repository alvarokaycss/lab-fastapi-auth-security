from typing import ClassVar

from pydantic_settings import BaseSettings
from sqlalchemy.orm import declarative_base


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    DB_URL: str  # Arquivo .env
    DBBaseModel: ClassVar = declarative_base()
    HOST: str = "127.0.0.1"
    PORT: int  # Arquivo .env
    RELOAD: bool = True
    LOG_LEVEL: str = "info"

    JWT_SECRET: str  # Arquivo .env
    """
    import secrets
    
    token: str = secrets.token_urlsafe(32)
    """
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 1 semana em minutos

    class Config:
        case_sensitive = True
        env_file = ".env"


settings: Settings = Settings()
