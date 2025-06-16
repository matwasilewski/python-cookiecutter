import time
from functools import lru_cache
from pathlib import Path
from typing import Optional, Union

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Settings. Environment variables always take priority over values loaded
    from the dotenv file.
    """

    current_timestamp: int = int(time.time())

    # Logger
    LOGGER_NAME: str = "{{cookiecutter.package_name}}"
    LOG_LEVEL: str = "info"
    VERBOSE_LOGS: Union[bool, int, str] = True
    JSON_LOGS: Union[bool, int, str] = False
    LOG_DIR: Path = (
        Path("logs") / f"{current_timestamp}-{LOGGER_NAME}-{LOG_LEVEL}.log"
    )

    SYSLOG_ADDR: Optional[Path] = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        secrets_dir = "secrets"


@lru_cache
def get_settings() -> Settings:
    return Settings(_env_file=f"{Path.cwd()}/.env")


settings = get_settings()
