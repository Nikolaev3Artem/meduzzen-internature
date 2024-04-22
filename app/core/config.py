from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    api_host: str
    api_port: int
    debug: bool
    origins: str

    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: str
    postgres_db: str

    postgres_test_host: str
    postgres_test_port: str
    postgres_test_db: str

    jwt_security_key: str

    @property
    def database_url(self):
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    @property
    def test_database_url(self):
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_test_host}:{self.postgres_test_port}/{self.postgres_test_db}"

    model_config = SettingsConfigDict(
        env_file=".env", _env_file_encoding="utf-8", extra="allow"
    )


settings = Settings()
