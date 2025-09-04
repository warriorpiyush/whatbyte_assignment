from django.contrib import admin
from .models import Doctor

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "specialization", "email", "phone", "created_at")
    search_fields = ("name", "email", "specialization")
