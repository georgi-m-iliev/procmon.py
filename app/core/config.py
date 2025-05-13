from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # Use top level .env file (one level above ./backend/)
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    PROJECT_NAME: str
    PROJECT_DESCRIPTION: str

    PROCESS_REFRESH_INTERVAL: int
    ANOMALY_THRESHOLD: float = 3.0
    ROLLING_WINDOW_SIZE: int = 30
    ROLLING_WINDOW_LIMIT: int = 5


settings = Settings()
