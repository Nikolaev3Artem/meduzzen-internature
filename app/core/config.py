from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Set

class Settings(BaseSettings):
    api_host: str
    api_port: int
    debug: bool
    origins: str

    model_config = SettingsConfigDict(env_file='.env', _env_file_encoding='utf-8', extra='allow')

settings = Settings()