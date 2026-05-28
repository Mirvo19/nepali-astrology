import sys
import logging

# Configure logging for Vercel functions
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# Initialize app variable before import (required by Vercel)
app = None
application = None

try:
    from application import create_app
    app = create_app()
    application = app
    logger.info("Flask application initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Flask application: {str(e)}", exc_info=True)
    
    # Create error handler WSGI app if initialization fails
    # This ensures Vercel doesn't fail with "app not found" error
    def error_handler(environ, start_response):
        status = '500 Internal Server Error'
        headers = [('Content-Type', 'application/json')]
        start_response(status, headers)
        return [b'{"error": "Failed to initialize application. Check logs for details."}']
    
    app = error_handler
    application = error_handler
