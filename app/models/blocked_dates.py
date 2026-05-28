from .db import get_public_client, get_admin_client


def list_blocked_dates(astrologer_id):
    client = get_public_client()
    return (
        client.table("blocked_dates")
        .select("*")
        .eq("astrologer_id", astrologer_id)
        .execute()
        .data
        or []
    )


def create_blocked_date(payload):
    client = get_admin_client()
    return client.table("blocked_dates").insert(payload).execute()


def delete_blocked_date(blocked_id):
    client = get_admin_client()
    return client.table("blocked_dates").delete().eq("id", blocked_id).execute()
