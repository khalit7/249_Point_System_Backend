from rest_framework import fields, serializers
from services.models import *


class customerRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerRequest
        fields = '__all__'

    def create(self, validated_data):
        time_due = validated_data['time_due']
        priority_level = validated_data['priority_level']
        customer = validated_data['customer']
        comments = validated_data['comments']
        service = validated_data['service']

        newRequest = CustomerRequest(
            service=service, customer=customer, time_due=time_due, priority_level=priority_level, comments=comments)
        newRequest.save()
        return newRequest

    def update(self, instance, validated_data):
        instance.is_confirmed = validated_data.get(
            'is_confirmed', instance.is_confirmed)
        instance.is_rejected = validated_data.get(
            'is_rejected', instance.is_rejected)
        instance.is_pending = validated_data.get(
            'is_pending', instance.is_pending)
        instance.save()
        return instance


class customerServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerService
        fields = '__all__'
