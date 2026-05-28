from flask import Flask, render_template, session, request
from .config import Config
from .blueprints.public.routes import public_bp
from .blueprints.bookings.routes import bookings_bp
from .blueprints.admin.routes import admin_bp
from .blueprints.api.routes import api_bp
from .models.site_settings import get_site_settings
from .utils.seo import render_seo
from .utils.static_hash import bust
import secrets


def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(Config)

    app.jinja_env.globals["bust"] = bust

    app.register_blueprint(public_bp)
    app.register_blueprint(bookings_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)

    @app.context_processor
    def inject_globals():
        site_settings = get_site_settings()
        seo = render_seo(site_settings=site_settings, current_path=request.path)
        return {
            "site_settings": site_settings,
            "seo": seo,
            "csrf_token": get_csrf_token(),
        }

    @app.errorhandler(404)
    def not_found(error):
        return render_template("public/404.html"), 404

    @app.errorhandler(500)
    def server_error(error):
        return render_template("public/500.html"), 500

    @app.after_request
    def set_cache_headers(response):
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
        return response

    return app


def get_csrf_token():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_urlsafe(24)
    return session["csrf_token"]
