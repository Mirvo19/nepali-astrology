from datetime import datetime, timedelta


def parse_time(value):
    if isinstance(value, str):
        return datetime.strptime(value, "%H:%M:%S").time()
    return value


def generate_slots(availability, blocked_dates, confirmed_bookings, date_str, duration_minutes):
    date_value = datetime.strptime(date_str, "%Y-%m-%d").date()
    if any(blocked.get("blocked_date") == date_str for blocked in blocked_dates):
        return []

    day_of_week = date_value.weekday()
    day_of_week = (day_of_week + 1) % 7

    slots = []
    booked_times = set()
    for booking in confirmed_bookings:
        time_value = booking.get("appointment_time")
        if isinstance(time_value, str) and len(time_value) >= 5:
            booked_times.add(time_value[:5])
        elif time_value:
            booked_times.add(time_value.strftime("%H:%M"))

    for entry in availability:
        if entry.get("day_of_week") != day_of_week:
            continue
        start_time = parse_time(entry.get("start_time"))
        end_time = parse_time(entry.get("end_time"))
        start_dt = datetime.combine(date_value, start_time)
        end_dt = datetime.combine(date_value, end_time)

        current = start_dt
        while current + timedelta(minutes=duration_minutes) <= end_dt:
            slot_time = current.time().strftime("%H:%M")
            if slot_time not in booked_times:
                slots.append(slot_time)
            current += timedelta(minutes=duration_minutes)

    return slots
