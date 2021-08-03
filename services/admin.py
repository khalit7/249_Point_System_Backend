from django.contrib import admin
from services.models import * 



class CustomerServicesAdmin(admin.ModelAdmin):
    list_display = ('type', )
    filter_horizontal = ()

class CustomerRequestsAdmin(admin.ModelAdmin):
    list_display = ('service' , 'customer' , 'priority_level','time_requested' , 'time_due','comments','is_pending','is_confirmed','is_rejected')
    filter_horizontal = ()
# Register your models here.

admin.site.register(CustomerRequest,CustomerRequestsAdmin)
admin.site.register(AdminRequest)
admin.site.register(CustomerService,CustomerServicesAdmin)
admin.site.register(AdminService)