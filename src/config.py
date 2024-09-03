from pydantic_settings import BaseSettings

from src.modules.utils import get_environment


class SecretSettings(BaseSettings):
    db_username: str
    db_password: str
    db_host: str
    db_dbname: str
    db_port: int

    redis_host: str
    redis_port: int

    jwt_secret_key: str

    class Config:
        env_file = f"./.env.{get_environment().lower()}"


secret_settings = SecretSettings()
