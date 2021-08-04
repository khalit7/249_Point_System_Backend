from datetime import date
from django.http import response
from django.http.response import HttpResponse
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes

from booking.models import DailySchedule, Resource, ResourceBooking
from services.models import CustomerService
from users.models import Customer

from booking.api.serializers import ResourceBookingSerializer,ResourceSerializer

from booking.api import custom_exceptions as custom_exceptions

def testView(request):
    return HttpResponse("I am booking API")


@api_view(['POST'])
def checkAvailabilityView(request):
    # JSON = {
    #     "capacity"
    #     "service"
    # }
    data = {}
    try:
        capacity = request.data['capacity']
        service = request.data['service']
    except KeyError:
        # handle error
        data['status'] = "failed"
        data['response message'] = "Wrong request"
        responseStatus = status.HTTP_400_BAD_REQUEST
        return Response(data=data, status=responseStatus)

    candidate_resources = Resource.objects.filter(
        service=service, capacity__gte=capacity, is_active=True)
    all_resources_availability = []
    for resource in candidate_resources:
        # check the availability
        dailyschedule = DailySchedule.objects.filter(resource=resource)
        availability = {}
        for day in dailyschedule:
            availability[day.date] = day.time_table
        all_resources_availability.append({"name": resource.name, "capacity": resource.capacity,
                                           "price per hour": resource.price_per_hour, "availability": availability})
    data['resources availability'] = all_resources_availability
    data['status'] = "success"
    data['response message'] = "successfully retrieved available resources"
    responseStatus = status.HTTP_200_OK
    return Response(data=data, status=responseStatus)


def checkResourceAvailability(resource):
    availability = {
        "this should include ... date (from now till on month after) : [list of all available times]"}

    all_bookings_on_resources = ResourceBooking.objects.filter(
        resource=resource)  # this should modify the list according to confirmed bookings

    return availability


@api_view(['POST'])
def bookView(request):
    JSON = {
        #resource
        #booking_date --> datetimefield
        #booked_for --> 24 literal string
    }
    data = {}
    serializer = ResourceBookingSerializer(data=request.data,partial=True)
    if serializer.is_valid():
        customer =Customer.objects.get(id=1)#request.user.customer
        try:
            serializer.save(customer = customer)
            data['booked_for'] = serializer.validated_data['booked_for']
            data['date'] =serializer.validated_data['booking_date']
            data['resource'] = serializer.validated_data['resource'].name
            data['status'] = 'success'
            data['response message'] = 'successfully requested the booking' 
            responseStatus = status.HTTP_200_OK
        except custom_exceptions.BookingNotAvailable as e:
            data['error'] = str(e)
            data['status'] = 'failed'
            data['response message'] = e.default_code
            responseStatus = status.HTTP_400_BAD_REQUEST
        except custom_exceptions.NotEnoughPoints as e:
            data['error'] = str(e)
            data['status'] = 'failed'
            data['response message'] = e.default_code
            responseStatus = status.HTTP_400_BAD_REQUEST
        
    else:
        data['error'] = serializer.errors
        data['status'] = 'failed'
        responseStatus = status.HTTP_400_BAD_REQUEST
    
    return Response(data=data,status = responseStatus)

@api_view(['GET'])
def getAllBookings (request):
    all_bookings = ResourceBooking.objects.filter(customer=request.user.customer)
    serializer = ResourceBookingSerializer(all_bookings,many =True)
    data = serializer.data
    responseStatus = status.HTTP_200_OK

    return Response(data=date,status=responseStatus)
    
@api_view(['GET'])
def getAllResources(request):
    all_resources  = Resource.objects.filter(is_active=True)
    serializer = ResourceSerializer(all_resources,many=True)
    data = serializer.data
    responseStatus = status.HTTP_200_OK

    return Response(data=data,status=responseStatus)
