from .db import get_public_client, get_admin_client
from ..utils.cache import get as cache_get, set as cache_set, invalidate


def list_gallery(visible_only=True):
    try:
        if visible_only:
            cached = cache_get("gallery:visible")
            if cached is not None:
                return cached
        client = get_public_client()
        query = client.table("gallery").select("*").order("sort_order")
        if visible_only:
            query = query.eq("is_visible", True)
        data = query.execute().data or []
        if visible_only:
            cache_set("gallery:visible", data, ttl=600)
        return data
    except Exception:
        return []


def create_or_update_gallery(payload, gallery_id=None):
    try:
        client = get_admin_client()
        if gallery_id:
            result = client.table("gallery").update(payload).eq("id", gallery_id).execute()
        else:
            result = client.table("gallery").insert(payload).execute()
        invalidate("gallery:visible")
        return result
    except Exception:
        return None


def delete_gallery(gallery_id):
    try:
        client = get_admin_client()
        result = client.table("gallery").delete().eq("id", gallery_id).execute()
        invalidate("gallery:visible")
        return result
    except Exception:
        return None
