from django.contrib import admin
from booking.models import *

class DailyScheduleAdmin(admin.ModelAdmin):
    
    list_display = ('resource','time_table', 'date')
    filter_horizontal = ()

class ResourceAdmin(admin.ModelAdmin):
    
    list_display = ('name','service', 'capacity','price_per_hour')
    filter_horizontal = ()

class ResourceBookingAdmin(admin.ModelAdmin):
    
    list_display = ('customer','resource','booking_date','booking_time','booked_for','total_number_of_hours','total_cost','is_pending','is_confirmed','is_rejected','created')
    filter_horizontal = ()
    def booking_time(self,resource_booking):
        is_tracking = False
        index_of_tracking_start=0
        booked_for = resource_booking.booked_for
        view_list = []
        for i in range(len(booked_for)):
            # 1.special cases 
            # when smoeone books the whole day
            if (booked_for.count('1') == 24):
                return "All-day"
            if (booked_for[i] == "1" and is_tracking==False):
                is_tracking=True
                index_of_tracking_start=i
            if (booked_for[i] == "0" and is_tracking == True ):
                view_list.append(str(index_of_tracking_start)+":00 - " + str(i) +":00")
                is_tracking=False
                index_of_tracking_start=0
            # 2.special cases 
            # when smoeone books the last hour of the day
            if (i==23 and booked_for[i]=="1"):
                view_list.append(str(index_of_tracking_start)+":00 - " + "23:59")
                
        return view_list
# Register your models here.

admin.site.register(Resource,ResourceAdmin)
admin.site.register(mentor)
admin.site.register(DailySchedule,DailyScheduleAdmin)
admin.site.register(ResourceBooking,ResourceBookingAdmin)