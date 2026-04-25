from functools import lru_cache

from dotenv import load_dotenv
from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    app_name: str = "API de ¿Ahí es?"
    api_prefix: str = "/api/v1"
    database_url: str = Field(
        default="postgresql+psycopg2://ahi_es:ahi_es@localhost:5432/ahi_es"
    )
    cors_origins_raw: str = "http://localhost:3000"
    dimension_min_score: int = -20
    dimension_max_score: int = 20

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @computed_field  # type: ignore[misc]
    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins_raw.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
