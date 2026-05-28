"""WSGI entrypoint for Vercel and production servers."""

from app import create_app

app = create_app()
application = app
