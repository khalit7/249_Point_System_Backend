from rest_framework.exceptions import APIException

class BookingNotAvailable(APIException):
    status_code = 400
    default_detail = 'Room not available at that date'
    default_code = 'room_unavailable'