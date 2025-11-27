from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.conf import settings
from account.manager import UserManager

class UserAuth(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name_plural = "All User"
        db_table = "user"   

    class Roles(models.TextChoices):
        ADMIN = 'ADMIN', 'ADMIN'
        USER = 'USER', 'USER'
        VENDOR = 'VENDOR', 'VENDOR'
        RIDER = 'RIDER', 'RIDER'
    full_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.USER)
    current_location = models.CharField(max_length=255,null=True, blank=True)
    current_address = models.CharField(max_length=255,null=True, blank=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_expired = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    objects = UserManager()

    def __str__(self):
        return self.email or self.phone_number

    @property
    def is_otp_valid(self):
        return self.otp and self.otp_expired and self.otp_expired > timezone.now()
    




class UserProfile(UserAuth):
    delivery_address = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Customer Profile"
        db_table = "user_profile"


class VendorProfile(UserAuth):
    shop_name = models.CharField(max_length=150, blank=True)
    shop_image = models.ImageField(upload_to='shop_image/', null=True, blank=True)
    shop_license = models.ImageField(upload_to='shop_license/', null=True, blank=True)
    shop_type = models.CharField(max_length=100, blank=True)
    shop_address = models.TextField(null=True, blank=True)
    rating = models.FloatField(default=0)
    total_rating_count = models.IntegerField(default=0)

    bank_name = models.CharField(max_length=100, blank=True)
    account_name = models.CharField(max_length=100, blank=True)
    account_number = models.CharField(max_length=100, blank=True)
    branch = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name_plural = "Vendor Profile"
        db_table = "vendor_profile"


class RiderProfile(UserAuth):
    rating = models.FloatField(default=0)
    vehicle_type = models.CharField(max_length=50, blank=True)
    license_number = models.CharField(max_length=100, blank=True)
    vehicle_plate = models.CharField(max_length=50, blank=True)

    bank_name = models.CharField(max_length=100, blank=True)
    account_name = models.CharField(max_length=100, blank=True)
    account_number = models.CharField(max_length=100, blank=True)
    branch = models.CharField(max_length=100, blank=True)

    rating = models.FloatField(default=0)
    total_rating_count = models.IntegerField(default=0)

    availability_status = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Rider Profile"
        db_table = "rider_profile"




class Banner(models.Model):
    vendor = models.ForeignKey(VendorProfile, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='banner_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.vendor.shop_name

    class Meta:
        verbose_name_plural = "Banner"
        db_table = "banner"