"""Delegate handler: import application from api.index so both files behave identically.

This avoids divergence between handlers and guarantees consistent initialization/logging.
"""
import sys
import logging
import importlib

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)

application = None

try:
    # Prefer to import local index module and reuse its `application` or `app`.
    idx = importlib.import_module("api.index")
    application = getattr(idx, "application", getattr(idx, "app", None))
    if application is None:
        raise RuntimeError("api.index did not expose 'application' or 'app'.")
    logger.info("Delegated WSGI application from api.index successfully.")
except Exception:
    logger.exception("Failed to delegate WSGI application from api.index")
    # Fallback handler that returns JSON error for failed startup
    def application(environ, start_response):
        status = "500 Internal Server Error"
        headers = [("Content-Type", "application/json")]
        start_response(status, headers)
        return [b'{"error": "Failed to initialize application. Check logs for details."}']
