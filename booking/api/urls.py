from django.urls import path
from booking.api import views_customers , views_admins


urlpatterns = [
    path("", views_customers.testView),
    # customer views
    path("checkAvailability/",views_customers.checkAvailability.as_view()),
    path("allResources/",views_customers.allResource.as_view()),
    path("book/",views_customers.bookView),
    path("allBookings/",views_customers.AllBookings),
    # admin views
    path("allBookingsAdmin/",views_admins.allBookingsAdmin.as_view()),
]
