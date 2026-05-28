from .db import get_public_client, get_admin_client


def create_booking(payload):
    try:
        client = get_admin_client()
        return client.table("bookings").insert(payload).execute()
    except Exception:
        return None


def get_booking_by_ref(booking_ref):
    try:
        client = get_admin_client()
        response = client.table("bookings").select("*").eq("booking_ref", booking_ref).limit(1).execute()
        return response.data[0] if response.data else None
    except Exception:
        return None


def list_bookings(filters=None):
    try:
        client = get_admin_client()
        query = client.table("bookings").select("*").order("created_at", desc=True)
        if filters:
            if filters.get("status"):
                query = query.eq("status", filters["status"])
            if filters.get("payment_status"):
                query = query.eq("payment_status", filters["payment_status"])
            if filters.get("astrologer_id"):
                query = query.eq("astrologer_id", filters["astrologer_id"])
            if filters.get("start_date"):
                query = query.gte("appointment_date", filters["start_date"])
            if filters.get("end_date"):
                query = query.lte("appointment_date", filters["end_date"])
        return query.execute().data or []
    except Exception:
        return []


def update_booking(booking_id, payload):
    try:
        client = get_admin_client()
        return client.table("bookings").update(payload).eq("id", booking_id).execute()
    except Exception:
        return None


def list_confirmed_bookings_by_date(astrologer_id, appointment_date):
    try:
        client = get_public_client()
        return (
            client.table("bookings")
            .select("appointment_time, status")
            .eq("astrologer_id", astrologer_id)
            .eq("appointment_date", appointment_date)
            .in_("status", ["confirmed", "pending"])
            .execute()
            .data
            or []
        )
    except Exception:
        return []
