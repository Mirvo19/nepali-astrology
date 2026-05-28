from .db import get_public_client, get_admin_client
from slugify import slugify
from ..utils.cache import get as cache_get, set as cache_set, invalidate, invalidate_prefix


def list_blog_posts(published_only=True):
    try:
        if published_only:
            cached = cache_get("blog:published")
            if cached is not None:
                return cached
        client = get_public_client()
        query = client.table("blog_posts").select("*").order("published_at", desc=True)
        if published_only:
            query = query.eq("is_published", True)
        data = query.execute().data or []
        if published_only:
            cache_set("blog:published", data, ttl=300)
        return data
    except Exception:
        return []


def get_blog_post_by_slug(slug, published_only=True):
    try:
        if published_only:
            cache_key = f"blog:{slug}"
            cached = cache_get(cache_key)
            if cached is not None:
                return cached
        client = get_public_client()
        query = client.table("blog_posts").select("*").eq("slug", slug)
        if published_only:
            query = query.eq("is_published", True)
        response = query.limit(1).execute()
        data = response.data[0] if response.data else None
        if published_only and data:
            cache_set(f"blog:{slug}", data, ttl=300)
        return data
    except Exception:
        return None


def create_or_update_post(payload, post_id=None):
    try:
        client = get_admin_client()
        if payload.get("title") and not payload.get("slug"):
            payload["slug"] = slugify(payload["title"])
        if post_id:
            result = client.table("blog_posts").update(payload).eq("id", post_id).execute()
        else:
            result = client.table("blog_posts").insert(payload).execute()
        invalidate("blog:published")
        invalidate_prefix("blog:")
        return result
    except Exception:
        return None


def delete_post(post_id):
    try:
        client = get_admin_client()
        result = client.table("blog_posts").delete().eq("id", post_id).execute()
        invalidate("blog:published")
        invalidate_prefix("blog:")
        return result
    except Exception:
        return None
