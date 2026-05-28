from flask import Flask, render_template, session, request
from .config import Config

try:
    from .blueprints.site.routes import public_bp
except ModuleNotFoundError:
    from .blueprints.public.routes import public_bp

from .blueprints.bookings.routes import bookings_bp
from .blueprints.admin.routes import admin_bp
from .blueprints.api.routes import api_bp
from .models.site_settings import get_site_settings
from .utils.seo import render_seo
from .utils.static_hash import bust
import os
import secrets
import logging

logger = logging.getLogger(__name__)


def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(Config)

    # Use signed cookie sessions on Vercel; filesystem sessions are not reliable there.
    if os.getenv("VERCEL") != "1":
        try:
            from flask_session import Session
            Session(app)
        except Exception as e:
            logger.warning(f"Failed to initialize Flask-Session: {e}. Using default sessions.")
    else:
        logger.info("Skipping Flask-Session on Vercel; using default signed cookie sessions.")

    app.jinja_env.globals["bust"] = bust

    # Register blueprints
    app.register_blueprint(public_bp)
    app.register_blueprint(bookings_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)

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
        return render_template("public/404.html"), 404

    @app.errorhandler(500)
    def server_error(error):
        logger.error(f"500 error: {error}", exc_info=True)
        return render_template("public/500.html"), 500

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
