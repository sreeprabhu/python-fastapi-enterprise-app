from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from enum import Enum

class DatabaseType(str, Enum):
    POSTGRES = "postgres"
    DYNAMODB = "dynamodb"

class Settings(BaseSettings):
    DATABASE_TYPE: DatabaseType = DatabaseType.POSTGRES # Default to postgres

    # --------------------------------------------------------------------
    # Postgres settings
    POSTGRES_DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@postgresql:5432/crypto_db"
    POSTGRES_DATABASE_URL_FOR_TESTING: str = "postgresql+asyncpg://postgres:postgres@postgresql:5432/crypto_db"
    # --------------------------------------------------------------------
    model_config = SettingsConfigDict(
        env_file = ".env",
        case_sensitive = True
    )

@lru_cache()
def get_settings() -> Settings:
    return Settings()


# Our Settings that implements Pydantic's BaseSettingsreads from our .envfile as per defined in model_config. 
# The get_settings method is used to return these settings, making them available in other parts of our application.