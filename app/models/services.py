from .db import get_public_client, get_admin_client
from ..utils.cache import get as cache_get, set as cache_set, invalidate_prefix


def list_services(astrologer_id=None, active_only=True):
    if astrologer_id and active_only:
        cache_key = f"services:{astrologer_id}"
        cached = cache_get(cache_key)
        if cached is not None:
            return cached
    client = get_public_client()
    query = client.table("services").select("*").order("sort_order")
    if astrologer_id:
        query = query.eq("astrologer_id", astrologer_id)
    if active_only:
        query = query.eq("is_active", True)
    data = query.execute().data or []
    if astrologer_id and active_only:
        cache_set(f"services:{astrologer_id}", data, ttl=300)
    return data


def get_service(service_id):
    client = get_public_client()
    response = client.table("services").select("*").eq("id", service_id).limit(1).execute()
    return response.data[0] if response.data else None


def create_or_update_service(payload, service_id=None):
    client = get_admin_client()
    if service_id:
        result = client.table("services").update(payload).eq("id", service_id).execute()
    else:
        result = client.table("services").insert(payload).execute()
    invalidate_prefix("services:")
    return result


def delete_service(service_id):
    client = get_admin_client()
    result = client.table("services").delete().eq("id", service_id).execute()
    invalidate_prefix("services:")
    return result
