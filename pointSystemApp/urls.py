from django.urls import  path
from pointSystemApp import views

urlpatterns = [
    path("",views.home,name="home"),
]
