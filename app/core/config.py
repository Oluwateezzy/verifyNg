from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    algorithm: str
    access_token_expire_minutes: int
    secret_key: str

    class Config:
        env_file = ".env"


settings = Settings()
