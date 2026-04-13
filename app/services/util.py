import uuid


def generate_unique_id():
    # Generate a 5-character unique id
    return str(uuid.uuid4())[:5]


def reservation_not_found_error():
    raise ValueError('Reservation not found')


def room_not_available_error():
    raise ValueError('Room is not available for the selected dates')


def date_lower_than_today_error():
    raise ValueError('Date cannot be lower than today')


def guest_not_found_error():
    raise ValueError('Guest not found')


def room_not_found_error():
    raise ValueError('Room not found')


def room_already_exists_error():
    raise ValueError('Room already exists')
