from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(BaseSettings):
    DEVELOPMENT: bool

    # Since we want to handle it by ourselves logic and load .env.examples if .env is not found.
    model_config = SettingsConfigDict(env_file=None)
