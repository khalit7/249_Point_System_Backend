from django.db import models
from django.db.models.enums import Choices
from users import models as UsersModels
# Create your models here.

PRIORITY_LEVELS = [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')]





class CustomerService(models.Model):
    CHOICES = [
        ('Room Booking Meeting', 'Room Booking Meeting'),
        ('Mentor meeting', 'Mentor meeting'),
        ('Workplace booking', 'Workplace booking')
    ]
    type = models.CharField(max_length=50, choices=CHOICES)
    description = models.TextField()

    def __str__(self):
        return self.type


class AdminService(models.Model):
    CHOICES = [
        ('Room Booking Meeting', 'Room Booking Meeting'),
        ('Mentor meeting', 'Mentor meeting'),
        ('Workplace booking', 'Workplace booking')
    ]
    type = models.CharField(max_length=50, choices=CHOICES)


class CustomerRequest(models.Model):
    service = models.ForeignKey(CustomerService, on_delete=models.CASCADE)
    time_requested = models.DateTimeField(auto_now_add=True)
    time_due = models.DateTimeField(auto_now=False, auto_now_add=False)
    customer = models.ForeignKey(
        UsersModels.Customer, on_delete=models.CASCADE)
    priority_level = models.CharField(max_length=20, choices=PRIORITY_LEVELS)
    comments = models.TextField()
    is_pending = models.BooleanField(default=True)
    is_confirmed = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)


class AdminRequest(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    time_requested = models.DateTimeField(auto_now_add=True)
    time_due = models.DateTimeField(auto_now=False, auto_now_add=False)
    admin = models.ForeignKey(UsersModels.Admin, on_delete=models.CASCADE)
    priority_level = models.CharField(max_length=30, choices=PRIORITY_LEVELS)
    comments = models.TextField()
