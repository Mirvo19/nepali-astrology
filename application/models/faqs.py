from .db import get_public_client, get_admin_client
from ..utils.cache import get as cache_get, set as cache_set, invalidate


def list_faqs(visible_only=True):
    try:
        if visible_only:
            cached = cache_get("faqs:visible")
            if cached is not None:
                return cached
        client = get_public_client()
        query = client.table("faqs").select("*").order("sort_order")
        if visible_only:
            query = query.eq("is_visible", True)
        data = query.execute().data or []
        if visible_only:
            cache_set("faqs:visible", data, ttl=600)
        return data
    except Exception:
        return []


def create_or_update_faq(payload, faq_id=None):
    try:
        client = get_admin_client()
        if faq_id:
            result = client.table("faqs").update(payload).eq("id", faq_id).execute()
        else:
            result = client.table("faqs").insert(payload).execute()
        invalidate("faqs:visible")
        return result
    except Exception:
        return None


def delete_faq(faq_id):
    try:
        client = get_admin_client()
        result = client.table("faqs").delete().eq("id", faq_id).execute()
        invalidate("faqs:visible")
        return result
    except Exception:
        return None
