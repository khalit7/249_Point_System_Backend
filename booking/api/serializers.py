from rest_framework import fields, serializers
from booking.models import *

from booking.api import custom_exceptions as custom_exceptions

from users.api.serializers import CustomerSerializer

import datetime


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'

class DailyScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailySchedule
        fields = '__all__'
    
    def update(self, instance, validated_data):
        instance.time_table = validated_data.get('time_table',instance.time_table)
        instance.save()
        return instance
class ResourceBookingSerializer(serializers.ModelSerializer):
    resource_serializer = ResourceSerializer(read_only=True)
    class Meta:
        model = ResourceBooking
        fields = '__all__'

    def create(self, validated_data):
        resource = validated_data['resource']
        resource_price_per_hour = resource.price_per_hour
        booked_for = validated_data['booked_for']
        booking_date = validated_data['booking_date']
        total_number_of_hours = booked_for.count('1')
        total_cost = total_number_of_hours*resource_price_per_hour
        customer = validated_data['customer']
        # check if there is a booking on the same time
        resource_schedule = DailySchedule.objects.get(
            resource=resource, date=int(booking_date.day))
        booking_checker = int(resource_schedule.time_table, base=2) & int(
            booked_for, base=2)
        if (booking_checker != 0):
            raise custom_exceptions.BookingNotAvailable()
        # if not ... make the new booking
        new_booking = ResourceBooking(customer=customer, resource=resource,
                                      booked_for=booked_for, total_number_of_hours=total_number_of_hours, total_cost=total_cost, booking_date=booking_date)
        # mark the resource as booked in that date
        updated_time_table = f'{int(resource_schedule.time_table,base=2) | int(booked_for,base=2):24b}'
        schedule_serializer = DailyScheduleSerializer(resource_schedule,data={'time_table' : updated_time_table} , partial = True)
        schedule_serializer.is_valid()
        #make sure the customer has enough points 
        if(customer.points<total_cost):
            raise custom_exceptions.NotEnoughPoints()
        #else
        remaining_points = customer.points - total_cost
        customer_serializer = CustomerSerializer(customer,data={'points':remaining_points},partial=True)
        customer_serializer.is_valid()
        # save everything
        customer_serializer.save()
        schedule_serializer.save()
        new_booking.save()
        return new_booking
