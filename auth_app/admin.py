from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('email', 'username', 'phone_number', 'town', 'is_donor', 'is_staff', 'date_joined', 'blood_group')
    list_filter = ('is_donor', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('email', 'username', 'phone_number', 'town')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'phone_number', 'town', 'blood_group')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Donor Info', {'fields': ('is_donor',)}),
        # ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'phone_number', 'town', 'is_donor', 'password1', 'password2', 'is_active', 'is_staff', 'blood_group')
        }),
    )

admin.site.register(User, UserAdmin)
