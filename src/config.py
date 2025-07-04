from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(BaseSettings):
    DEVELOPMENT: bool
    SUPER_SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(..., gt=0)

    # Since we want to handle it by ourselves logic and load .env.examples if .env is not found.
    model_config = SettingsConfigDict(env_file=None)
