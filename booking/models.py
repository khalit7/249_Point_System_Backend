from django.db import models
from django.db.models.base import Model
from django.db.models.fields import DateTimeField
from users.models import Customer
from services.models import CustomerService

import datetime
# Create your models here.


# resources to be booked
class Resource(models.Model):
    CHOICES_name = [
        ('Room1', 'Room1'),
        ('Room2', 'Room2'),
        ('Room3','Room3'),
        ('Workplace1', 'Workplace1')
    ]
    CHOICES_service = [
        ('meeting', 'meeting'),
        ('workplace', 'workplace')
    ]
    name = models.CharField(max_length=50, choices=CHOICES_name)
    service = models.CharField(max_length=50,choices=CHOICES_service)
    capacity = models.IntegerField()
    price_per_hour = models.FloatField()
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name

class DailySchedule(models.Model):
    # 0 means empty , 1 means occupied ... 1 number for every hour in the day
    time_table = models.CharField(max_length=24)
    date = models.IntegerField()
    resource = models.ForeignKey(Resource,  on_delete=models.CASCADE)

    def __Str__(self):
        return "Daily schedule day " + self.date

    # def parseTimeTable(self,time_table):
    #     parsed_time_table = {} #{string  hours: bool isAvailable}
    #     for i in range(0,24): # 0-23 hours of the day
    #         parsed_time_table[str(i)] = False
    #     # loop through self.time_table to update the parsed_time_table
    #     for hour in self.time_table:
    #         if(hour)=='0':
    #             parsed_time_table[hour] == True
    #     return parsed_time_table


class mentor (models.Model):
    name = models.CharField(max_length=50)


class ResourceBooking (models.Model):
    customer = models.ForeignKey(Customer,  on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, null=True)
    booked_for = models.CharField(max_length=24,null=True)
    booking_date = models.DateField(default=datetime.date.today)
    total_number_of_hours = models.IntegerField(null=True,blank=True)
    total_cost = models.FloatField(null=True,blank=True)   
    created = models.DateField(auto_now_add=True) 
    is_pending = models.BooleanField(default=True)
    is_confirmed = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)



class mentorMeeting (models.Model):
    pass
