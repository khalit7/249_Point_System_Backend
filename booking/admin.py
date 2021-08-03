from django.contrib import admin
from booking.models import *

class DailyScheduleAdmin(admin.ModelAdmin):
    
    list_display = ('resource','time_table', 'date')
    filter_horizontal = ()

class ResourceAdmin(admin.ModelAdmin):
    
    list_display = ('name','service', 'capacity','price_per_hour')
    filter_horizontal = ()

class ResourceBookingAdmin(admin.ModelAdmin):
    
    list_display = ('customer','resource', 'booked_for','booking_date','total_number_of_hours','total_cost','is_pending','is_confirmed','is_rejected','created')
    filter_horizontal = ()
# Register your models here.

admin.site.register(Resource,ResourceAdmin)
admin.site.register(mentor)
admin.site.register(DailySchedule,DailyScheduleAdmin)
admin.site.register(ResourceBooking,ResourceBookingAdmin)