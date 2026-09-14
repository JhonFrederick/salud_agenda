from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import AdminProfile, MedicProfile, PatientProfile, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role Info', {'fields': ('role',)}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')


@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    search_fields = ('user__username', 'user__email')


@admin.register(MedicProfile)
class MedicProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'license_number', 'specialty')
    search_fields = ('user__username', 'user__email', 'license_number', 'specialty')


@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date_of_birth', 'phone_number')
    search_fields = ('user__username', 'user__email', 'phone_number')
