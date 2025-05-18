from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Level

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('phone_number', 'username', 'level', 'elo', 'is_staff')
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Personal info', {'fields': ('username',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Additional info', {'fields': ('level', 'elo')}),
    )
    search_fields = ('phone_number', 'username')
    ordering = ('phone_number',)

admin.site.register(User, CustomUserAdmin)
admin.site.register(Level)
