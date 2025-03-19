from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    algorithm: str
    access_token_expire_minutes: int
    secret_key: str
    do_spaces_access_key: str
    do_spaces_secret: str
    do_spaces_bucket: str
    do_spaces_endpoint: str
    do_spaces_region: str
    mailtrap_username: str
    mailtrap_password: str
    mailtrap_host: str
    mailtrap_port: int

    class Config:
        env_file = ".env"


settings = Settings()
