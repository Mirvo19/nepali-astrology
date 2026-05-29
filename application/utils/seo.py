from datetime import datetime, timezone
from flask import current_app
from ..models.astrologers import list_astrologers
from ..models.blog_posts import list_blog_posts


def render_seo(site_settings, current_path, meta_override=None):
    """
    Render SEO context with fallback defaults optimized for nepali astrology keywords.
    """
    meta = {
        "meta_title": site_settings.get("meta_title")
        or "nepali astrology — vedic kundali readings & consultations online",
        "meta_description": site_settings.get("meta_description")
        or "connect with expert nepali astrologers for vedic kundali readings, rashifal, vastu, and jyotish consultations. book your online astrology session today.",
        "og_image": site_settings.get("og_image_url")
        or "https://www.nepaliastrology.com/static/assets/og-default.jpg",
        "contact_phone": site_settings.get("contact_phone") or "",
        "current_path": current_path,
        "site_url": current_app.config.get("SITE_URL", "https://www.nepaliastrology.com"),
    }
    if meta_override:
        meta.update(meta_override)
    return meta
