from django.http import response
from django.http.response import HttpResponse
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny


from users.api.serializers import AccountSerializer
from users.models import Account, Admin, Customer, FacilityResponsible


@api_view(['GET'])
def testView(request):
    return Response(data={'1': '1'})

# api/users/signup/


@api_view(['POST'])
@authentication_classes([])
def signup(request):
    #  JSON = {
    #      "email":
    #      "username":
    #      "password":
    #       "password2"
    #      "role":
    #       "Admin role"
    #       "Customer role"
    #       "Facility Responsible role"
    #  }
    serializer = AccountSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        data = serializer.validated_data
        data['status'] = "success"
        data['response message'] = 'user successfully created'
        data['error'] = ''
        serializer.save()
        responseStatus = status.HTTP_201_CREATED
    else:
        data['error'] = serializer.errors
        data['status'] = 'failed'
        responseStatus = status.HTTP_400_BAD_REQUEST

    return Response(data=data, status=responseStatus)

# api/users/me/


@api_view(['GET'])
def getUserDetails(request):
    data = {}
    userObject = Account.objects.get(id=request.user.id)

    serializer = AccountSerializer(userObject)
    data = serializer.data

    if (userObject.role == 'Customer'):
        data['points'] = userObject.customer.points
        data['customer role'] = userObject.customer.role
    if (userObject.role == 'Admin'):
        data['admin role'] = userObject.admin.role
    if (userObject.role == "Facility Manager"):
        data['facility manager role'] = userObject.facilityResponsible.role

    return Response(data=data)
