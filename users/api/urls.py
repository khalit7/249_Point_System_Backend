from django.urls import path
from users.api import views


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# api/users/...
urlpatterns = [
    path("", views.testView),
    # path("login", views.login_view),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #
    path('signup/',views.signup),
    path('me/',views.getUserDetails),
]
