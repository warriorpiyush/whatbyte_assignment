from django.contrib import admin
from .models import PatientDoctor

@admin.register(PatientDoctor)
class PatientDoctorAdmin(admin.ModelAdmin):
    list_display = ("id", "patient", "doctor", "created_at")
    search_fields = ("patient__name", "doctor__name")