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
        exclude = ['password','last_login','is_superuser','is_staff','is_active','date_joined','groups','user_permissions','otp','otp_expired','is_approved']

class VendorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorProfile
        # fields = '__all__'
        exclude = ['password','last_login','is_superuser','is_staff','is_active','date_joined','groups','user_permissions','otp','otp_expired','is_approved']


class CombinedUserSerializer(serializers.Serializer):
    user_type = serializers.CharField()
    full_name = serializers.CharField()
    email = serializers.EmailField()
    phone_number = serializers.CharField()
    image = serializers.ImageField(required=False)
    role = serializers.CharField()
    address = serializers.CharField(required=False)
    rating = serializers.FloatField(required=False)
    shop_name = serializers.CharField(required=False)
    shop_image = serializers.ImageField(required=False)
    shop_license = serializers.ImageField(required=False)
    shop_type = serializers.CharField(required=False)
    shop_address = serializers.CharField(required=False)
    vehicle_type = serializers.CharField(required=False)
    license_number = serializers.CharField(required=False)
    vehicle_plate = serializers.CharField(required=False)
    availability_status = serializers.BooleanField(required=False)
    bank_name = serializers.CharField(required=False)
    account_name = serializers.CharField(required=False)
    account_number = serializers.CharField(required=False)
    branch = serializers.CharField(required=False)

    def to_representation(self, instance):
        if isinstance(instance, VendorProfile):
            return {
                "id": instance.id,
                "full_name": instance.full_name,
                "email": instance.email,
                "phone_number": instance.phone_number,
                "image": instance.image.url if instance.image else None,
                "role": instance.role,
                "shop_name": instance.shop_name,
                "shop_image": instance.shop_image.url if instance.shop_image else None,
                "shop_license": instance.shop_license.url if instance.shop_license else None,
                "shop_type": instance.shop_type,
                "shop_address": instance.shop_address,
                "rating": instance.rating,
                "bank_name": instance.bank_name,
                "account_name": instance.account_name,
                "account_number": instance.account_number,
                "branch": instance.branch,
            }
        elif isinstance(instance, UserProfile):
            return {
                "id": instance.id,
                "full_name": instance.full_name,
                "email": instance.email,
                "phone_number": instance.phone_number,
                "image": instance.image.url if instance.image else None,
                "role": instance.role,
                "address": instance.address,
            }
        elif isinstance(instance, RiderProfile):
            return {
                "id": instance.id,
                "full_name": instance.full_name,
                "email": instance.email,
                "phone_number": instance.phone_number,
                "image": instance.image.url if instance.image else None,
                "role": instance.role,
                "rating": instance.rating,
                "vehicle_type": instance.vehicle_type,
                "license_number": instance.license_number,
                "vehicle_plate": instance.vehicle_plate,
                "availability_status": instance.availability_status,
                "bank_name": instance.bank_name,
                "account_name": instance.account_name,
                "account_number": instance.account_number,
                "branch": instance.branch,
            }
        return super().to_representation(instance)