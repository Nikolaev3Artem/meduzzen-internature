from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    api_host: str
    api_port: int
    debug: bool 
    origins: str

    model_config = SettingsConfigDict(env_file='.env', _env_file_encoding='utf-8')

settings = Settings(_env_file='.env', _env_file_encoding='utf-8')