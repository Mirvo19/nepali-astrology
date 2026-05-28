"""Local development entrypoint.

Do not name this file app.py — that shadows the app/ package on Vercel.
Use wsgi.py for deployment (see vercel.json).
"""
import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=os.environ.get("FLASK_ENV") == "development",
    )
