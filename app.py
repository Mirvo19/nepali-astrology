"""Vercel / WSGI entrypoint. Root app.py must not share a name with the Flask package (application/)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from application import create_app

app = create_app()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=os.environ.get("FLASK_ENV") == "development",
    )
