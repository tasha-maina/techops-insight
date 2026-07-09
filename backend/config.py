import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    DARAJA_CONSUMER_KEY = os.getenv("DARAJA_CONSUMER_KEY")
    DARAJA_CONSUMER_SECRET = os.getenv("DARAJA_CONSUMER_SECRET")
    DARAJA_BASE_URL = os.getenv("DARAJA_BASE_URL")
    DARAJA_SHORTCODE = os.getenv("DARAJA_SHORTCODE")
    DARAJA_PASSKEY = os.getenv("DARAJA_PASSKEY")
    DARAJA_CALLBACK_URL = os.getenv("DARAJA_CALLBACK_URL")

    SMTP_HOST = os.getenv("SMTP_HOST")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
    SMTP_USERNAME = os.getenv("SMTP_USERNAME")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
    SMTP_USE_TLS = os.getenv("SMTP_USE_TLS", "true").lower() in ("1", "true", "yes")
    EMAIL_FROM = os.getenv("EMAIL_FROM")
    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
    EMAIL_ENABLED = os.getenv("EMAIL_ENABLED", "false").lower() in ("1", "true", "yes")

    @classmethod
    def require_core_vars(cls):
        required = [
            "DATABASE_URL",
            "SECRET_KEY",
            "JWT_SECRET_KEY"
        ]
        missing = [env for env in required if os.getenv(env) is None]
        if missing:
            raise RuntimeError(
                f"Missing required environment variables: {', '.join(missing)}"
            )
