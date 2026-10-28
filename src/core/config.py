"""Application configuration and environment variable loading."""

import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

# Base directory (project root: d:\Devsinc)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load .env file
load_dotenv(BASE_DIR / ".env")


@dataclass(frozen=True)
class Settings:
    """Immutable application settings populated from environment variables."""

    app_env: str = os.getenv("APP_ENV", "development")
    debug: bool = os.getenv("APP_DEBUG", "true").lower() in ("true", "1", "yes")
    log_level: str = os.getenv("APP_LOG_LEVEL", "INFO").upper()
    default_max_hours_per_week: float = float(
        os.getenv("DEFAULT_MAX_HOURS_PER_WEEK", "40.0")
    )


settings = Settings()
