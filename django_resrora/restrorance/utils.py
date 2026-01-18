# utils.py
from .models import Booking

def is_room_available(room_type, check_in, check_out):
    """
    Returns True if there is at least one room available of the given type
    for the requested check-in/check-out dates.
    """
    booked_count = Booking.objects.filter(
        room_type=room_type,
        status='BOOKED',
        check_in__lt=check_out,
        check_out__gt=check_in
    ).count()

    return booked_count < room_type.total_rooms
 