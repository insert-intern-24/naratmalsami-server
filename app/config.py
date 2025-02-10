from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    google_client_id: str
    google_client_secret: str
    secret_key: str
    mysql_url: str

    class Config:
        env_file = ".env"

settings = Settings()
