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
    DATABASE_URL: str = Field(min_length=1, repr=False)

    API_KEY: str = Field(default="cure-secret-master-key", repr=False)
    EMBEDDING_MODEL_ID: str = Field(default="BAAI/bge-m3")
    EMBEDDING_MODEL_PATH: str = Field(default="models/bge-m3")
    EMBEDDING_DEVICE: str = Field(default="cuda")

    @property
    def resolved_model_path(self) -> Path:
        path = Path(self.EMBEDDING_MODEL_PATH)
        return path if path.is_absolute() else PROJECT_ROOT / path



@lru_cache
def get_settings() -> Settings:
    """Load settings once and reuse them across requests."""
    return Settings()


settings = get_settings()