from .db import get_public_client, get_admin_client


def list_availability(astrologer_id):
    try:
        client = get_public_client()
        return (
            client.table("availability")
            .select("*")
            .eq("astrologer_id", astrologer_id)
            .eq("is_active", True)
            .execute()
            .data
            or []
        )
    except Exception:
        return []


def create_or_update_availability(payload, availability_id=None):
    try:
        client = get_admin_client()
        if availability_id:
            return client.table("availability").update(payload).eq("id", availability_id).execute()
        return client.table("availability").insert(payload).execute()
    except Exception:
        return None


def delete_availability(availability_id):
    try:
        client = get_admin_client()
        return client.table("availability").delete().eq("id", availability_id).execute()
    except Exception:
        return None
