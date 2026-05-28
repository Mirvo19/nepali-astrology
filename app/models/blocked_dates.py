from .db import get_public_client, get_admin_client


def list_blocked_dates(astrologer_id):
    try:
        client = get_public_client()
        return (
            client.table("blocked_dates")
            .select("*")
            .eq("astrologer_id", astrologer_id)
            .execute()
            .data
            or []
        )
    except Exception:
        return []


def create_blocked_date(payload):
    try:
        client = get_admin_client()
        return client.table("blocked_dates").insert(payload).execute()
    except Exception:
        return None


def delete_blocked_date(blocked_id):
    try:
        client = get_admin_client()
        return client.table("blocked_dates").delete().eq("id", blocked_id).execute()
    except Exception:
        return None
