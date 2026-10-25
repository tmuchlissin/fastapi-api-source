from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


PROJECT_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        extra="ignore",
    )
    
    TEST_BEARER_TOKEN: str = Field(min_length=1, repr=False)



@lru_cache
def get_settings() -> Settings:
    """Load settings once and reuse them across requests."""
    return Settings()


settings = get_settings()