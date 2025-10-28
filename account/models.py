from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from account.manager import UserManager

class UserAuth(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name_plural = "Users"

    class Roles(models.TextChoices):
        ADMIN = 'Admin', 'Admin'
        USER = 'User', 'User'
        VENDOR = 'Vendor', 'Vendor'
        RIDER = 'Rider', 'Rider'

    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.USER)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_expired = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'phone_number']

    objects = UserManager()

    def __str__(self):
        return self.full_name or self.email

    @property
    def is_otp_valid(self):
        return self.otp and self.otp_expired and self.otp_expired > timezone.now()
