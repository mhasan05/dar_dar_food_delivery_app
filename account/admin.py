from django.contrib import admin
from account.models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

admin.site.unregister(Group)
class UserAuthAdmin(UserAdmin):
    model = UserAuth
    list_display = ('email', 'phone_number', 'role', 'is_active')
    search_fields = ('email','phone_number')
    ordering = ('email',)

    fieldsets = (
        ('Login Credentials', {'fields': ('email','phone_number', 'password')}),
        ('Role & Permissions', {'fields': ('role', 'is_active','is_approved', 'is_staff', 'is_superuser')}),
        ('OTP', {'fields': ('otp', 'otp_expired')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'role', 'password1', 'password2', 'is_active','is_approved', 'is_staff', 'is_superuser')
        }),
    )
    
admin.site.register(UserAuth,UserAuthAdmin)





class UserProfileAdmin(UserAdmin):
    model = UserProfile
    list_display = ('email', 'phone_number', 'role', 'is_active')
    search_fields = ('email','phone_number')
    ordering = ('email',)

    fieldsets = (
        ('Login Credentials', {'fields': ('email','phone_number', 'password')}),
        ('Personal Info', {'fields': ('image','address')}),
        ('Role & Permissions', {'fields': ('role', 'is_active')}),
        ('OTP', {'fields': ('otp', 'otp_expired')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','phone_number', 'role','image','address', 'password1', 'password2', 'is_active')
        }),
    )
    
admin.site.register(UserProfile,UserProfileAdmin)




class RiderProfileAdmin(UserAdmin):
    model = RiderProfile
    list_display = ('email', 'phone_number', 'role', 'is_active')
    search_fields = ('email','phone_number')
    ordering = ('email',)

    fieldsets = (
        ('Login Credentials', {'fields': ('email','phone_number', 'password')}),
        ('Personal Info', {'fields': ('image','rating')}),
        ('Vehicle Info', {'fields': ('vehicle_type', 'license_number', 'vehicle_plate','availability_status')}),
        ('Role & Permissions', {'fields': ('role', 'is_active')}),
        ('OTP', {'fields': ('otp', 'otp_expired')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','phone_number', 'role','image','rating','vehicle_type', 'license_number', 'vehicle_plate','availability_status', 'password1', 'password2', 'is_active')
        }),
    )
    
admin.site.register(RiderProfile,RiderProfileAdmin)




class VendorProfileAdmin(UserAdmin):
    model = VendorProfile
    list_display = ('email', 'phone_number', 'role', 'is_active')
    search_fields = ('email','phone_number')
    ordering = ('email',)

    fieldsets = (
        ('Login Credentials', {'fields': ('email','phone_number', 'password')}),
        ('Personal Info', {'fields': ('image','shop_name','shop_type','shop_address','rating','bank_name','account_name','account_number','branch')}),
        ('Role & Permissions', {'fields': ('role', 'is_active')}),
        ('OTP', {'fields': ('otp', 'otp_expired')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','phone_number', 'role','image','shop_name','shop_type','shop_address','rating','bank_name','account_name','account_number','branch', 'password1', 'password2', 'is_active')
        }),
    )
    
admin.site.register(VendorProfile,VendorProfileAdmin)