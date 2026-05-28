import sys
import logging

# Configure startup logging for serverless runtime diagnostics
logging.basicConfig(
	level=logging.INFO,
	format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
	stream=sys.stdout,
)
logger = logging.getLogger(__name__)

app = None
application = None

try:
	from app import create_app

	app = create_app()
	application = app
	logger.info("Root wsgi.py initialized Flask app successfully")
except Exception as e:
	logger.error(f"Root wsgi.py failed to initialize Flask app: {e}", exc_info=True)

	# Keep a valid WSGI callable so runtime returns controlled error output.
	def application(environ, start_response):
		status = "500 Internal Server Error"
		headers = [("Content-Type", "application/json")]
		start_response(status, headers)
		return [b'{"error":"Application startup failed. See server logs."}']

	app = application
