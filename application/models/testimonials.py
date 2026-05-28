from .db import get_public_client, get_admin_client
from ..utils.cache import get as cache_get, set as cache_set, invalidate


def list_testimonials(visible_only=True):
    try:
        if visible_only:
            cached = cache_get("testimonials:visible")
            if cached is not None:
                return cached
        client = get_public_client()
        query = client.table("testimonials").select("*").order("created_at", desc=True)
        if visible_only:
            query = query.eq("is_visible", True)
        data = query.execute().data or []
        if visible_only:
            cache_set("testimonials:visible", data, ttl=600)
        return data
    except Exception:
        return []


def create_or_update_testimonial(payload, testimonial_id=None):
    try:
        client = get_admin_client()
        if testimonial_id:
            result = client.table("testimonials").update(payload).eq("id", testimonial_id).execute()
        else:
            result = client.table("testimonials").insert(payload).execute()
        invalidate("testimonials:visible")
        return result
    except Exception:
        return None


def delete_testimonial(testimonial_id):
    try:
        client = get_admin_client()
        result = client.table("testimonials").delete().eq("id", testimonial_id).execute()
        invalidate("testimonials:visible")
        return result
    except Exception:
        return None
