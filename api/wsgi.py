import sys
import logging
from app import create_app

# Configure logging for Vercel functions
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

try:
    app = create_app()
    # Vercel expects 'application' as the WSGI app
    application = app
    logger.info("Flask application initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Flask application: {str(e)}", exc_info=True)
    raise
