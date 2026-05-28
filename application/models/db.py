from supabase import create_client
from flask import current_app

_public_client = None
_admin_client = None


def get_public_client():
    global _public_client
    if _public_client is not None:
        return _public_client
    url = current_app.config.get("SUPABASE_URL")
    key = current_app.config.get("SUPABASE_ANON_KEY")
    _public_client = create_client(url, key)
    return _public_client


def get_admin_client():
    global _admin_client
    if _admin_client is not None:
        return _admin_client
    url = current_app.config.get("SUPABASE_URL")
    key = current_app.config.get("SUPABASE_KEY")
    _admin_client = create_client(url, key)
    return _admin_client
