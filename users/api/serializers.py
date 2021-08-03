from rest_framework import fields, serializers
from users.models import *
from django.conf import settings


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['username', 'email', 'date_joined', 'role','password']
        extra_kwargs = {
            'password':{'write_only': True},
        }
    
    def save(self, ):
        validated_data = self.validated_data
        username = validated_data['username']
        password = validated_data['password']
        email = validated_data['email']
        role = validated_data['role']
        newAccount = Account.objects.create_user(username=username,email=email,role=role,password=password)
        
        if (role == "Admin"): 
            newAccount.is_admin = True
            newAdmin = Admin (user = newAccount)
            newAdmin.save()
        if (role == "Customer"):
            newCustomer = Customer(user = newAccount, points = 0.0)
            newCustomer.save()
        if (role == "Facility Manager"):
            facilityManager = FacilityResponsible()
            facilityManager.save()
        newAccount.save()
        
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.points = validated_data.get('points',instance.points)
        instance.save()
        return instance