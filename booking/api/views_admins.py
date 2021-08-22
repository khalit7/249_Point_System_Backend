from datetime import date
from django.http import response
from django.http.response import HttpResponse
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.generics import GenericAPIView, ListAPIView

from booking.models import DailySchedule, Resource, ResourceBooking
from services.models import CustomerService
from users.models import Customer

from booking.api.serializers import ResourceBookingSerializer, ResourceSerializer

from booking.api import custom_exceptions as custom_exceptions


def testView(request):
    return HttpResponse("I am booking API")


class allBookingsAdmin (ListAPIView) : 
    serializer_class = ResourceBookingSerializer

    def get_queryset(self):
        queryset = ResourceBooking.objects.all()
        return queryset
    
    def get(self, request, *args, **kwargs):
        data = {}
        allBookings = self.get_queryset()
        serializer = ResourceBookingSerializer(allBookings,many=True)
        data['all_bookings'] = serializer.data
        data['status'] = 'success'
        data['response message'] = "successfully retrieved all bookings"
        responseStatus = status.HTTP_200_OK
        return Response(data=data,status=responseStatus)
