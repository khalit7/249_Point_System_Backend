from django.urls import path
from services.api import views


urlpatterns = [
    path("", views.testView),

    #

    path('request/', views.requestServiceView),
    path('allSevices/', views.getAllServicesView),
    path('myRequests/', views.myRequestesView),
    path('AllRequests/', views.getAllRequestsView),
    path('respondToRequestByid/',views.respondToRequestView),
    path('addPoints/',views.addPointsView)
]
