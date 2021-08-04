from rest_framework.exceptions import APIException

class BookingNotAvailable(APIException):
    status_code = 400
    default_detail = 'Room not available at that date'
    default_code = 'room_unavailable'

class NotEnoughPoints(APIException):
    status_code = 400
    default_detail = 'You dont have enough points to undergo this transaction'
    default_code = 'insufficient_points'