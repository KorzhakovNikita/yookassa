import logging

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    SERVER_HOST: str
    SERVER_PORT: int
    CORS_ALLOWED_ORIGINS: list[str]

    # Database
    DATABASE_URL: str
    DATABASE_ECHO: bool
    DATABASE_POOL_SIZE: int
    DATABASE_MAX_OVERFLOW: int
    DATABASE_POOL_PRE_PING: bool

    # Yookassa
    SHOP_ID: int
    SHOP_SECRET_KEY: str


settings = Settings(_env_file=".env", _env_file_encoding="utf-8")


def configure_logging(level: str = logging.INFO):
    logging.basicConfig(
        level=level,
        datefmt="%Y-%m-%d %H:%M:%S:",
        format="[%(asctime)s.%(msecs)03d] %(module)s:%(lineno)d %(levelname)s - %(message)s"
    )