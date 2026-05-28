from .db import get_public_client, get_admin_client
from slugify import slugify
from ..utils.cache import get as cache_get, set as cache_set, invalidate, invalidate_prefix


def list_astrologers(active_only=True):
    if active_only:
        cached = cache_get("astrologers:list")
        if cached is not None:
            return cached
    client = get_public_client()
    query = client.table("astrologers").select("*").order("sort_order")
    if active_only:
        query = query.eq("is_active", True)
    data = query.execute().data or []
    if active_only:
        cache_set("astrologers:list", data, ttl=300)
    return data


def get_astrologer_by_slug(slug):
    cache_key = f"astrologer:{slug}"
    cached = cache_get(cache_key)
    if cached is not None:
        return cached
    client = get_public_client()
    response = client.table("astrologers").select("*").eq("slug", slug).limit(1).execute()
    data = response.data[0] if response.data else None
    if data:
        cache_set(cache_key, data, ttl=300)
    return data


def create_or_update_astrologer(payload, astrologer_id=None):
    client = get_admin_client()
    if payload.get("name") and not payload.get("slug"):
        payload["slug"] = slugify(payload["name"])
    if astrologer_id:
        result = client.table("astrologers").update(payload).eq("id", astrologer_id).execute()
    else:
        result = client.table("astrologers").insert(payload).execute()
    invalidate("astrologers:list")
    invalidate_prefix("astrologer:")
    return result


def delete_astrologer(astrologer_id):
    client = get_admin_client()
    result = client.table("astrologers").delete().eq("id", astrologer_id).execute()
    invalidate("astrologers:list")
    invalidate_prefix("astrologer:")
    return result
