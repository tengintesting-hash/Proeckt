from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Telegram Social Platform"
    env: str = "development"
    database_url: str
    redis_url: str
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_access_ttl_minutes: int = 60
    jwt_refresh_ttl_minutes: int = 60 * 24 * 7
    telegram_bot_token: str
    telegram_webapp_secret: str
    media_root: str = "/data/media"
    support_url: str = "https://t.me/support"
    privacy_url: str = "https://example.com/privacy"
    terms_url: str = "https://example.com/terms"
    eighteen_plus_url: str = "https://example.com/18plus"
    ml_service_url: str = "http://ml-service:9000"
    admin_telegram_id: int | None = None

    class Config:
        env_file = ".env"


settings = Settings()
