import os

from flask import Blueprint, render_template, request, Response, redirect, url_for, current_app, jsonify
from ...models.astrologers import list_astrologers, get_astrologer_by_slug
from ...models.services import list_services
from ...models.testimonials import list_testimonials
from ...models.faqs import list_faqs
from ...models.blog_posts import list_blog_posts, get_blog_post_by_slug
from ...models.gallery import list_gallery
from ...utils.seo import render_seo, generate_sitemap, generate_robots

public_bp = Blueprint("public", __name__)


@public_bp.route("/debug-templates")
def debug_templates():
    tf = current_app.template_folder
    results = {
        "template_folder_config": tf,
        "template_folder_resolved": os.path.abspath(tf) if tf else None,
        "template_folder_exists": os.path.isdir(tf) if tf else False,
        "cwd": os.getcwd(),
        "var_task_contents": os.listdir("/var/task") if os.path.exists("/var/task") else [],
        "files_found": []
    }
    if tf and os.path.isdir(tf):
        for root, dirs, files in os.walk(tf):
            for f in files:
                results["files_found"].append(
                    os.path.join(root, f).replace(tf, "")
                )
    return jsonify(results)


@public_bp.route("/")
def home():
    astrologers = list_astrologers(active_only=True)
    testimonials = list_testimonials(visible_only=True)
    faqs = list_faqs(visible_only=True)
    posts = list_blog_posts(published_only=True)[:3]
    gallery = list_gallery(visible_only=True)
    return render_template(
        "home.html",
        astrologers=astrologers,
        testimonials=testimonials,
        faqs=faqs,
        posts=posts,
        gallery=gallery,
    )


@public_bp.route("/astrologers")
def astrologers():
    astrologers_list = list_astrologers(active_only=True)
    services = list_services()
    services_map = {}
    service_names = sorted({service["name"] for service in services})
    for service in services:
        services_map.setdefault(service["astrologer_id"], []).append(service["name"])
    return render_template(
        "astrologers.html",
        astrologers=astrologers_list,
        services=services,
        service_names=service_names,
        services_map=services_map,
    )


@public_bp.route("/astrologers/<slug>")
def astrologer_profile(slug):
    astrologer = get_astrologer_by_slug(slug)
    services = list_services(astrologer_id=astrologer["id"]) if astrologer else []
    seo = render_seo(
        site_settings={"meta_title": astrologer.get("name") if astrologer else "Astrologer"},
        current_path=request.path,
        meta_override={"meta_title": astrologer.get("name") if astrologer else "Astrologer"},
    )
    return render_template(
        "astrologer_profile.html",
        astrologer=astrologer,
        services=services,
        seo=seo,
    )


@public_bp.route("/blog")
def blog_index():
    posts = list_blog_posts(published_only=True)
    seo = render_seo(
        site_settings={"meta_title": "Astrology Blog"},
        current_path=request.path,
        meta_override={"meta_title": "Astrology Blog"},
    )
    return render_template("blog.html", posts=posts, seo=seo)


@public_bp.route("/blog/<slug>")
def blog_post(slug):
    post = get_blog_post_by_slug(slug, published_only=True)
    meta_title = post.get("meta_title") if post else "Astrology Insights"
    meta_description = post.get("meta_description") if post else "Astrology insights"
    seo = render_seo(
        site_settings={"meta_title": meta_title, "meta_description": meta_description},
        current_path=request.path,
        meta_override={"meta_title": meta_title, "meta_description": meta_description},
    )
    return render_template("blog_post.html", post=post, seo=seo)


@public_bp.route("/about")
def about():
    astrologers_list = list_astrologers(active_only=True)
    return render_template("about.html", astrologers=astrologers_list)


@public_bp.route("/contact")
def contact():
    return render_template("contact.html")


@public_bp.route("/favicon.ico")
def favicon():
    return redirect(url_for("static", filename="assets/favicon.ico"), code=301)


@public_bp.route("/sitemap.xml")
def sitemap():
    xml = generate_sitemap()
    return Response(xml, mimetype="application/xml")


@public_bp.route("/robots.txt")
def robots():
    content = generate_robots()
    return Response(content, mimetype="text/plain")
