from flask import Blueprint, request, jsonify, abort, session
from app.models.astrologers import list_astrologers
from app.models.availability import list_availability
from app.models.blocked_dates import list_blocked_dates
from app.models.bookings import list_confirmed_bookings_by_date, create_booking
from app.models.services import get_service
from app.utils.slots import generate_slots
from app.utils.mailer import send_contact_message
from app.models.site_settings import get_site_settings
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

api_bp = Blueprint("api", __name__, url_prefix="/api")


def validate_csrf():
    token = request.headers.get("X-CSRF-Token")
    return token and token == session.get("csrf_token")


@api_bp.route("/slots/<astrologer_id>")
def slots(astrologer_id):
    try:
        date_str = request.args.get("date")
        service_id = request.args.get("service_id")
        if not date_str or not service_id:
            abort(400)
        service = get_service(service_id)
        if not service:
            abort(404)
        availability = list_availability(astrologer_id)
        blocked = list_blocked_dates(astrologer_id)
        bookings = list_confirmed_bookings_by_date(astrologer_id, date_str)
        slots_list = generate_slots(
            availability,
            blocked,
            bookings,
            date_str,
            int(service.get("duration_minutes", 60)),
        )
        return jsonify({"slots": slots_list})
    except Exception as e:
        logger.error(f"Error in /slots endpoint: {e}", exc_info=True)
        return jsonify({"error": "Failed to generate slots"}), 500


@api_bp.route("/astrologers")
def astrologers():
    try:
        astrologers_list = list_astrologers(active_only=True)
        return jsonify(astrologers_list)
    except Exception as e:
        logger.error(f"Error in /astrologers endpoint: {e}", exc_info=True)
        return jsonify({"error": "Failed to fetch astrologers"}), 500


@api_bp.route("/book", methods=["POST"])
def book():
    try:
        if not validate_csrf():
            abort(400)
        payload = request.json or {}
        if not payload.get("client_name"):
            abort(400)
        payload["status"] = "pending"
        payload["payment_status"] = "unpaid"
        payload["created_at"] = datetime.utcnow().isoformat()
        create_booking(payload)
        return jsonify({"status": "ok"})
    except Exception as e:
        logger.error(f"Error in /book endpoint: {e}", exc_info=True)
        return jsonify({"error": "Failed to create booking"}), 500


@api_bp.route("/contact", methods=["POST"])
def contact():
    try:
        if not validate_csrf():
            abort(400)
        payload = request.json or {}
        site = get_site_settings()
        sent = send_contact_message(site.get("contact_email"), payload)
        if not sent:
            return jsonify({"status": "error", "message": "Service temporarily unavailable."}), 503
        return jsonify({"status": "sent"})
    except Exception as e:
        logger.error(f"Error in /contact endpoint: {e}", exc_info=True)
        return jsonify({"error": "Failed to send message"}), 500
