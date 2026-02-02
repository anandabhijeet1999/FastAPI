from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    mongodb_uri: str = "mongodb://localhost:27017"
    db_name: str = "hrms_lite"
    cors_origins: str = "https://classy-bienenstitch-8b8297.netlify.app/"
    mongodb_tls_insecure: bool = False


settings = Settings()

