import argparse
from functools import lru_cache
from typing import Optional

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ["get_config"]


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # server
    HOST: str = Field(validate_default=False)
    PORT: int = Field(validate_default=False)
    WORKER: int = Field(validate_default=False)
    RELOAD: bool = Field(validate_default=False)

    # Postgres
    POSTGRES_HOST: str = Field(validate_default=False, default="0.0.0.0")
    POSTGRES_PORT: int = Field(validate_default=False, default=5433)
    POSTGRES_USER: str = Field(validate_default=False, default="postgres")
    POSTGRES_PASSWORD: SecretStr = Field(
        validate_default=False, default=SecretStr("postgres")
    )
    POSTGRES_DB: str = Field(validate_default=False, default="tmparch")

    # Redis
    REDIS_HOST: str = Field(validate_default=False, default="0.0.0.0")
    REDIS_PORT: int = Field(validate_default=False, default=6379)
    REDIS_USER: str = Field(validate_default=False, default="default")
    REDIS_PASSWORD: SecretStr = Field(
        validate_default=False, default=SecretStr("password")
    )
    REDIS_DB: str = Field(validate_default=False, default="0")

    # Rabbitmq
    RABBITMQ_HOST: str = Field(validate_default=False, default="0.0.0.0")
    RABBITMQ_PORT: int = Field(validate_default=False, default=5671)
    RABBITMQ_USER: str = Field(validate_default=False, default="rabbit")
    RABBITMQ_PASSWORD: SecretStr = Field(
        validate_default=False, default=SecretStr("password")
    )

    RABBITMQ_QUEUE: str = Field(validate_default=False, default="main")

    # kuber
    HEALTHCHECK: bool = False

    # system
    CMD: Optional[str] = None
    TESTING: bool = False


def arg_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--cmd",
        "-c",
        choices=[
            "Http",
            "HttpLock",
            "AdminRabbitConsumer",
            "AdminExec",
        ],
        default="Http",
        required=False,
    )
    parser.add_argument("*", nargs="*")
    args, _ = parser.parse_known_args()
    return args


@lru_cache()
def get_config() -> Config:
    settings = Config()  # type: ignore
    if settings.TESTING is True:
        return settings

    arg_map = arg_parser()
    settings.CMD = arg_map.cmd
    return settings
