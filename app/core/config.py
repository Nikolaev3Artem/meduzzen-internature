from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    api_host: str
    api_port: int
    debug: bool 

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

settings = Settings()