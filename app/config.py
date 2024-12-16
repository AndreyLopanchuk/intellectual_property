from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseSettings):
    url: str = "postgresql+asyncpg://admin:admin@db/library"


class Settings(BaseModel):
    model_config = SettingsConfigDict(case_sensitive=False)
    db: PostgresSettings = PostgresSettings()


settings = Settings()
