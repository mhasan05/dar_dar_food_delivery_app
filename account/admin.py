from django.contrib import admin
from account.models import UserAuth
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group


class UserAuthAdmin(UserAdmin):
    model = UserAuth
    list_display = ('email', 'phone_number', 'role', 'is_active')
    search_fields = ('email','phone_number')
    ordering = ('email',)

    fieldsets = (
        ('Login Credentials', {'fields': ('email','phone_number', 'password')}),
        ('Personal Info', {'fields': ('image',)}),
        ('Role & Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser')}),
        ('OTP', {'fields': ('otp', 'otp_expired')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'role', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser')
        }),
    )
    
admin.site.register(UserAuth,UserAuthAdmin)
admin.site.unregister(Group)