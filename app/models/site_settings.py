from .db import get_public_client, get_admin_client
from ..utils.cache import get as cache_get, set as cache_set, invalidate


def get_site_settings():
    cached = cache_get("settings:global")
    if cached:
        return cached
    client = get_public_client()
    response = client.table("site_settings").select("*").limit(1).execute()
    if response.data:
        data = response.data[0]
        cache_set("settings:global", data, ttl=600)
        return data
    data = {
        "site_name": "Nepali Astrology",
        "tagline": "Vedic guidance for modern life",
        "hero_heading": "Discover your cosmic path",
        "hero_subheading": "Kundali readings, rashifal insights, numerology & vastu guidance from trusted Nepali astrologers.",
        "hero_cta_text": "Book a session",
        "about_text": "We blend ancient Vedic wisdom with compassionate guidance for your life journey.",
        "about_image_url": "",
        "contact_email": "hello@nepaliastrology.com",
        "contact_phone": "+977-000000000",
        "contact_address": "Kathmandu, Nepal",
        "whatsapp_number": "+977-000000000",
        "facebook_url": "",
        "instagram_url": "",
        "youtube_url": "",
        "meta_title": "Nepali Astrology | Vedic Astrology, Kundali & Rashifal",
        "meta_description": "Book trusted Nepali astrologers for kundali readings, rashifal, numerology, and vastu guidance.",
        "og_image_url": "",
        "footer_text": "© 2026 Nepali Astrology. All rights reserved.",
    }
    cache_set("settings:global", data, ttl=600)
    return data


def update_site_settings(payload):
    client = get_admin_client()
    existing = client.table("site_settings").select("id").limit(1).execute()
    if existing.data:
        setting_id = existing.data[0]["id"]
        result = client.table("site_settings").update(payload).eq("id", setting_id).execute()
    else:
        result = client.table("site_settings").insert(payload).execute()
    invalidate("settings:global")
    return result
