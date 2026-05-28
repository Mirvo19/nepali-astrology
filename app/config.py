import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Required
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY") or os.environ.get("SECRET_KEY")
    SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
    SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")
    SUPABASE_ANON_KEY = os.environ.get("SUPABASE_ANON_KEY", "")

    # Runtime
    FLASK_ENV = os.environ.get("FLASK_ENV", "production")
    DEBUG = FLASK_ENV == "development"
    TESTING = False
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)

    # Payment (optional at startup)
    STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "")
    STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET", "")

    # Email (optional)
    SMTP_HOST = os.environ.get("SMTP_HOST", "")
    smtp_port = os.environ.get("SMTP_PORT", "587")
    SMTP_PORT = int(smtp_port) if smtp_port.isdigit() else 587
    SMTP_USER = os.environ.get("SMTP_USER", "")
    SMTP_PASS = os.environ.get("SMTP_PASS", "")
    ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "")

    # Site
    SITE_URL = os.environ.get("SITE_URL", "https://nepaliastrology.com")
    TIMEZONE = "Asia/Kathmandu"

    @classmethod
    def validate(cls):
        missing = []
        for key in ["SECRET_KEY", "SUPABASE_URL", "SUPABASE_KEY"]:
            if not getattr(cls, key):
                missing.append(key)
        if missing:
            raise RuntimeError(f"missing required env vars: {', '.join(missing)}")
