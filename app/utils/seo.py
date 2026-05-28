from datetime import datetime
from flask import current_app
from ..models.astrologers import list_astrologers
from ..models.blog_posts import list_blog_posts


def render_seo(site_settings, current_path, meta_override=None):
    meta = {
        "meta_title": site_settings.get("meta_title") or site_settings.get("site_name"),
        "meta_description": site_settings.get("meta_description") or site_settings.get("tagline"),
        "og_image": site_settings.get("og_image_url") or "",
        "contact_phone": site_settings.get("contact_phone") or "",
        "current_path": current_path,
        "site_url": current_app.config.get("SITE_URL"),
    }
    if meta_override:
        meta.update(meta_override)
    return meta


def generate_sitemap():
    base_url = current_app.config.get("SITE_URL")
    urls = [
        "",
        "/about",
        "/contact",
        "/blog",
        "/astrologers",
    ]
    astrologers = list_astrologers(active_only=True)
    for astro in astrologers:
        urls.append(f"/astrologers/{astro['slug']}")
    posts = list_blog_posts(published_only=True)
    for post in posts:
        urls.append(f"/blog/{post['slug']}")

    lastmod = datetime.utcnow().date().isoformat()
    items = "".join(
        [
            f"<url><loc>{base_url}{path}</loc><lastmod>{lastmod}</lastmod></url>"
            for path in urls
        ]
    )
    return (
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
        "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">"
        f"{items}"
        "</urlset>"
    )


def generate_robots():
    base_url = current_app.config.get("SITE_URL")
    return f"User-agent: *\nAllow: /\nSitemap: {base_url}/sitemap.xml\n"
