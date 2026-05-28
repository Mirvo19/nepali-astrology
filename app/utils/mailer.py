import smtplib
from email.mime.text import MIMEText
from flask import current_app


def send_email(to_email, subject, html_body):
    try:
        host = current_app.config.get("SMTP_HOST")
        port = current_app.config.get("SMTP_PORT")
        user = current_app.config.get("SMTP_USER")
        password = current_app.config.get("SMTP_PASS")

        if not host or not user or not password:
            return False

        message = MIMEText(html_body, "html")
        message["Subject"] = subject
        message["From"] = user
        message["To"] = to_email

        with smtplib.SMTP(host, port) as server:
            server.starttls()
            server.login(user, password)
            server.sendmail(user, [to_email], message.as_string())
        return True
    except Exception:
        return False


def send_booking_confirmation(to_email, booking):
    subject = "Your Nepali Astrology booking is confirmed"
    html_body = f"""
    <h2>Booking Confirmed</h2>
    <p>Namaste {booking.get('client_name')},</p>
    <p>Your session has been confirmed. We will see you on {booking.get('appointment_date')} at {booking.get('appointment_time')}.</p>
    <p>Booking reference: {booking.get('booking_ref')}</p>
    """
    return send_email(to_email, subject, html_body)


def send_contact_message(to_email, payload):
    subject = "New contact enquiry"
    html_body = f"""
    <h2>Contact Enquiry</h2>
    <p><strong>Name:</strong> {payload.get('name')}</p>
    <p><strong>Email:</strong> {payload.get('email')}</p>
    <p><strong>Message:</strong> {payload.get('message')}</p>
    """
    return send_email(to_email, subject, html_body)
