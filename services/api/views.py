from django.http.response import HttpResponse
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes
from django.contrib.auth import authenticate


from services.api.serializers import customerRequestSerializer, customerServiceSerializer
from users.api.serializers import CustomerSerializer
from services.models import *
import users
from users.models import Account, Customer


def testView(request):
    return HttpResponse("I am Servics API")


@api_view(['POST'])
def respondToRequestView(request):
    # JSON = {
    #      "response"
    #      "requestID"
    # }
    data = {}
    try:
        response = request.data['response']
        requestid = request.data['requestID']
    except KeyError:
        data['error'] = "unknown request"
        data['status'] = 'failed'
        responseStatus = status.HTTP_400_BAD_REQUEST
        return Response(data=data, status=responseStatus)

    customerRequstToUpdate = CustomerRequest.objects.get(id=requestid)
    if(customerRequstToUpdate.is_pending == False):
        data['error'] = "Already responded to this request"
        data['status'] = 'failed'
        responseStatus = status.HTTP_400_BAD_REQUEST
        return Response(data=data, status=responseStatus)

    if response == "confirm":
        serializer = customerRequestSerializer(customerRequstToUpdate, data={
            "is_confirmed": "True", "is_pending": "False"}, partial=True)
        serializer.is_valid()
        serializer.save()
        data['status'] = "success"
        data['response message'] = "successfully confirmed the request"
        responseStatus = status.HTTP_200_OK
    elif response == "reject":
        serializer = customerRequestSerializer(customerRequstToUpdate, data={
            "is_rejected": "True", "is_pending": "False"}, partial=True)
        serializer.is_valid()
        serializer.save()
        # return points to the customer making the request
        servicePrice = customerRequstToUpdate.service.price
        customer = customerRequstToUpdate.customer
        pointsAfterRefund = servicePrice + customer.points
        serializer = CustomerSerializer(
            customer, data={"points": pointsAfterRefund}, partial=True)
        serializer.is_valid()
        serializer.save()
        data['status'] = "success"
        data['response message'] = "successfully rejected the request"
        responseStatus = status.HTTP_200_OK
    else:  # error
        data['error'] = "unknown request"
        data['status'] = 'failed'
        responseStatus = status.HTTP_400_BAD_REQUEST

    return Response(data=data, status=responseStatus)


@api_view(['POST'])
def addPointsView(request):
    # JSON = {
    #       "points"
    #       "username"
    # }
    data = {}
    try:
        username = request.data['username']
        pointsToAdd = float(request.data['points'])
    except:
        data['error'] = "unknown request"
        data['status'] = 'failed'
        responseStatus = status.HTTP_400_BAD_REQUEST
        return Response(data=data,status=responseStatus)

    customerToUpdate = Account.objects.get(username=username).customer
    pointsAfterUpdate = customerToUpdate.points + pointsToAdd
    serializer = CustomerSerializer(customerToUpdate,data={"points":pointsAfterUpdate},partial=True)
    serializer.is_valid()
    serializer.save()
    data['status'] = "success"
    data['response message'] = "successfully added " + str(pointsToAdd) + " points to " + username
    return Response(data=data)


@api_view(['GET'])
def myRequestesView(request):
    allRequests = CustomerRequest.objects.filter(
        customer=request.user.customer)
    serializer = customerRequestSerializer(allRequests, many=True)

    data = serializer.data
    responseStatus = status.HTTP_200_OK

    return Response(data=data, status=responseStatus)


@api_view(['GET'])
def getAllServicesView(request):
    allServices = CustomerService.objects.all()
    serializer = customerServiceSerializer(allServices, many=True)

    data = serializer.data
    responseStatus = status.HTTP_200_OK

    return Response(data=data, status=responseStatus)


@api_view(['GET'])
# TODO:add admin permisson
def getAllRequestsView(request):
    allRequests = CustomerRequest.objects.all()
    serializer = customerRequestSerializer(allRequests, many=True)

    data = serializer.data
    responseStatus = status.HTTP_200_OK

    return Response(data=data, status=responseStatus)


@api_view(['POST'])
def requestServiceView(request):
    # JSON = {
    #     "type"
    #     "time_due"
    #     "priority_level"
    #     "comments"
    # }
    data = {}

    serviceSerializer = customerServiceSerializer(
        data=request.data, partial=True)

    if serviceSerializer.is_valid():
        service = CustomerService.objects.get(
            type=serviceSerializer.validated_data['type'])
    else:
        data['error'] = serviceSerializer.errors
        data['status'] = "failed"
        responseStatus = status.HTTP_400_BAD_REQUEST
        return Response(data=data, status=responseStatus)

    if service.price > request.user.customer.points:
        # dont have enough credit
        data['error'] = 'sorry, you dont have enough credit'
        data['status'] = "failed"
        responseStatus = status.HTTP_400_BAD_REQUEST
        return Response(data=data, status=responseStatus)
    # else : perform the request

    serializer = customerRequestSerializer(data=request.data, partial=True)

    if serializer.is_valid():
        newRequest = serializer.save(
            customer=request.user.customer, service=service)
        data = customerRequestSerializer(newRequest).data
        data['status'] = 'success'
        data['response message'] = 'successfully created the request'
        responseStatus = status.HTTP_200_OK
        # deduct points
        remainingPoints = request.user.customer.points - service.price
        updatedCustomer = CustomerSerializer(
            request.user.customer, data={'points': remainingPoints}, partial=True)
        updatedCustomer.is_valid()
        updatedCustomer.save()
        data['points'] = remainingPoints
    else:
        data['error'] = serializer.errors
        data['status'] = "failed"
        responseStatus = status.HTTP_400_BAD_REQUEST

    return Response(data=data, status=responseStatus)
