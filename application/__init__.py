import os

from flask import Flask, render_template, session, request

from .config import Config

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


from .blueprints.site.routes import public_bp

from .blueprints.bookings.routes import bookings_bp
from .blueprints.admin.routes import admin_bp
from .blueprints.api.routes import api_bp
from .models.site_settings import get_site_settings
from .utils.seo import render_seo
from .utils.static_hash import register_bust
import secrets
import logging
import sys

logger = logging.getLogger(__name__)


def create_app():
    if not logging.getLogger().handlers:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[logging.StreamHandler(sys.stdout)],
        )
    app = Flask(
        __name__,
        template_folder=os.path.join(BASE_DIR, "templates"),
        static_folder=os.path.join(BASE_DIR, "static"),
    )
    app.config.from_object(Config)
    Config.validate()
    app.permanent_session_lifetime = app.config["PERMANENT_SESSION_LIFETIME"]

    register_bust(app)

    # Register blueprints (raise on failure with full trace)
    try:
        app.register_blueprint(public_bp)
        app.register_blueprint(bookings_bp)
        app.register_blueprint(admin_bp)
        app.register_blueprint(api_bp)
    except Exception as e:
        logger.error("Failed to register blueprints", exc_info=True)
        raise

    @app.context_processor
    def inject_globals():
        try:
            site_settings = get_site_settings()
        except Exception as e:
            logger.error(f"Error loading site settings: {e}")
            site_settings = {}
        
        try:
            seo = render_seo(site_settings=site_settings, current_path=request.path)
        except Exception as e:
            logger.error(f"Error rendering SEO: {e}")
            seo = {}
        
        return {
            "site_settings": site_settings,
            "seo": seo,
            "csrf_token": get_csrf_token(),
        }

    @app.errorhandler(404)
    def not_found(error):
        logger.warning(f"404 error: {request.path}")
        try:
            return render_template("public/404.html"), 404
        except Exception:
            return """<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>page not found</title>
<style>body{background:#080808;color:#e8e2d4;font-family:sans-serif;display:flex;align-items:center;justify-content:center;min-height:100vh;margin:0;flex-direction:column;gap:16px;}
h1{font-size:48px;color:#c4a050;margin:0;}p{color:#9a9080;margin:0;}</style></head>
<body><h1>404</h1><p>this page does not exist.</p>
<a href="/" style="color:#c4a050;text-decoration:none;font-size:14px;">← return home</a></body>
</html>""", 404

    @app.errorhandler(500)
    def server_error(error):
        logger.error(f"500 error: {error}", exc_info=True)
        try:
            return render_template("public/500.html"), 500
        except Exception:
            return """<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>server error</title>
<style>body{background:#080808;color:#e8e2d4;font-family:sans-serif;display:flex;align-items:center;justify-content:center;min-height:100vh;margin:0;flex-direction:column;gap:16px;}
h1{font-size:48px;color:#c4a050;margin:0;}p{color:#9a9080;margin:0;}</style></head>
<body><h1>500</h1><p>something went wrong. please try again shortly.</p>
<a href="/" style="color:#c4a050;text-decoration:none;font-size:14px;">← return home</a></body>
</html>""", 500

    @app.after_request
    def set_cache_headers(response):
        try:
            if "/static/" in request.path and "?v=" in request.query_string.decode():
                response.cache_control.max_age = 31536000
                response.cache_control.public = True
                response.cache_control.immutable = True
            elif "/static/" in request.path:
                response.cache_control.max_age = 3600

            if request.path == "/" or request.path.startswith("/blog") or request.path.startswith("/astrologers"):
                response.cache_control.no_store = False
                response.cache_control.max_age = 300
                response.cache_control.public = True
        except Exception as e:
            logger.error(f"Error setting cache headers: {e}")
        
        return response

    return app


def get_csrf_token():
    try:
        if "csrf_token" not in session:
            session["csrf_token"] = secrets.token_urlsafe(24)
        return session["csrf_token"]
    except Exception as e:
        logger.warning(f"Failed to get CSRF token: {e}")
        return ""
