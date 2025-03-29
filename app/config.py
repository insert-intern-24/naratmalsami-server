from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv(".env", override=True)

class Settings(BaseSettings):
    google_client_id: str
    google_client_secret: str
    secret_key: str
    mysql_url: str
    debug: bool = False
    is_dev: bool = True
    discord_webhook_general: str = ""
    discord_webhook_alert: str = ""
    hashids_salt: str = "default_salt"
    hashids_min_length: int = 6
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
