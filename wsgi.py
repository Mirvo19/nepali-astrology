from app import create_app

app = create_app()

# vercel expects this
application = app
