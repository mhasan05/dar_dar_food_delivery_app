from rest_framework import serializers
from account.models import *


class AdminProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAuth
        # fields = '__all__'
        exclude = ['password','last_login','is_superuser','is_staff','is_active','date_joined','groups','user_permissions','otp','otp_expired','is_approved']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        # fields = '__all__'
        exclude = ['password','last_login','is_superuser','is_staff','is_active','date_joined','groups','user_permissions','otp','otp_expired','is_approved']

class RiderProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiderProfile
        # fields = '__all__'
        exclude = ['password','last_login','is_superuser','is_staff','is_active','date_joined','groups','user_permissions','otp','otp_expired']

class VendorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorProfile
        # fields = '__all__'
        exclude = ['password','last_login','is_superuser','is_staff','is_active','date_joined','groups','user_permissions','otp','otp_expired']