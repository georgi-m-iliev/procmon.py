from typing import Literal, Any, Annotated

from pydantic import AnyUrl, BeforeValidator, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


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

    CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []

    @computed_field  # type: ignore[prop-decorator]
    @property
    def all_cors_origins(self) -> list[str]:
        if self.ENVIRONMENT == "local":
            return ["*"]
        return [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS]


settings = Settings()
