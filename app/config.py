from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    google_client_id: str
    google_client_secret: str
    secret_key: str
    mysql_url: str
    debug: bool = False
    discord_webhook_general: str = ""
    discord_webhook_alert: str = ""
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
