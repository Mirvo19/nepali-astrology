from flask import Blueprint, render_template, request, redirect, url_for, session, abort
from datetime import datetime, timezone
from ...models.astrologers import get_astrologer_by_slug
from ...models.services import get_service
from ...models.bookings import create_booking, get_booking_by_ref
from ...utils.mailer import send_booking_confirmation

bookings_bp = Blueprint("bookings", __name__)


def validate_csrf():
    token = request.form.get("csrf_token")
    return token and token == session.get("csrf_token")


def generate_booking_ref():
    now_utc = datetime.now(tz=timezone.utc)
    suffix = now_utc.strftime("%H%M%S")
    date_part = now_utc.strftime("%Y%m%d")
    return f"NA-{date_part}-{suffix}"


@bookings_bp.route("/book/<astrologer_slug>/<service_id>", methods=["GET", "POST"])
def book(astrologer_slug, service_id):
    astrologer = get_astrologer_by_slug(astrologer_slug)
    service = get_service(service_id)
    if not astrologer or not service:
        abort(404)

    if request.method == "POST":
        if not validate_csrf():
            abort(400)

        payload = {
            "booking_ref": generate_booking_ref(),
            "astrologer_id": astrologer["id"],
            "service_id": service["id"],
            "client_name": request.form.get("client_name"),
            "client_email": request.form.get("client_email"),
            "client_phone": request.form.get("client_phone"),
            "client_birth_date": request.form.get("client_birth_date"),
            "client_birth_time": request.form.get("client_birth_time"),
            "client_birth_place": request.form.get("client_birth_place"),
            "appointment_date": request.form.get("appointment_date"),
            "appointment_time": request.form.get("appointment_time"),
            "notes": request.form.get("notes"),
            "status": "pending",
            "payment_status": "unpaid",
            "amount_npr": service.get("price_npr"),
        }
        create_booking(payload)
        return redirect(url_for("bookings.checkout", booking_ref=payload["booking_ref"]))

    return render_template(
        "bookings/book.html",
        astrologer=astrologer,
        service=service,
    )


@bookings_bp.route("/checkout/<booking_ref>")
def checkout(booking_ref):
    booking = get_booking_by_ref(booking_ref)
    if not booking:
        abort(404)
    return render_template("bookings/checkout.html", booking=booking)


@bookings_bp.route("/booking/confirm/<booking_ref>")
def confirm(booking_ref):
    booking = get_booking_by_ref(booking_ref)
    if not booking:
        abort(404)
    if booking.get("payment_status") == "paid":
        send_booking_confirmation(booking.get("client_email"), booking)
    return render_template("bookings/confirm.html", booking=booking)
