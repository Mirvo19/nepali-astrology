import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY") or "dev_secret"
    
    # Session configuration - use memory-based for Vercel compatibility
    # Filesystem sessions don't work on Vercel's ephemeral filesystem
    SESSION_TYPE = "filesystem"
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    PERMANENT_SESSION_LIFETIME = 3600
    
    # Database configuration
    SUPABASE_URL = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
    SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "")
    
    # Payment configuration
    STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")
    STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")
    
    # Email configuration
    SMTP_HOST = os.getenv("SMTP_HOST", "")
    smtp_port = os.getenv("SMTP_PORT", "587")
    SMTP_PORT = int(smtp_port) if smtp_port.isdigit() else 587
    SMTP_USER = os.getenv("SMTP_USER", "")
    SMTP_PASS = os.getenv("SMTP_PASS", "")
    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "")
    
    # Site configuration
    SITE_URL = os.getenv("SITE_URL", "https://nepaliastrology.com")
    TIMEZONE = "Asia/Kathmandu"
