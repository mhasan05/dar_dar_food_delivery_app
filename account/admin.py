from django.contrib import admin
from account.models import UserAuth
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group


class UserAuthAdmin(UserAdmin):
    model = UserAuth
    list_display = ('full_name', 'email', 'phone_number', 'role', 'is_active')
    search_fields = ('full_name','email','phone_number')

    fieldsets = (
        ('Login Credentials', {'fields': ('email','phone_number', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'image')}),
        ('Role & Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser')}),
        ('OTP', {'fields': ('otp', 'otp_expired')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'role', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser')
        }),
    )
    
admin.site.register(UserAuth,UserAuthAdmin)
admin.site.unregister(Group)