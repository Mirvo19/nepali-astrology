from supabase import create_client
from flask import current_app


def get_public_client():
    url = current_app.config.get("SUPABASE_URL")
    key = current_app.config.get("SUPABASE_ANON_KEY")
    return create_client(url, key)


def get_admin_client():
    url = current_app.config.get("SUPABASE_URL")
    key = current_app.config.get("SUPABASE_KEY")
    return create_client(url, key)
