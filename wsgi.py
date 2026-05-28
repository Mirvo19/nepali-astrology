"""WSGI alias for gunicorn and legacy hosts."""

from application import create_app

app = create_app()
application = app
