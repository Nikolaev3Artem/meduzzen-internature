from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    api_host: str
    api_port: int
    debug: bool 
    postgres_user: str
    postgres_password: str
    postgres_server: str
    postgres_port: str
    postgres_db: str
    model_config = SettingsConfigDict(env_file='.env', _env_file_encoding='utf-8', extra='allow')

settings = Settings()