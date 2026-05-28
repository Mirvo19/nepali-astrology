"""Legacy compatibility module.

Canonical deployment entrypoint is app.py.
"""

from app import create_app

app = create_app()
application = app
