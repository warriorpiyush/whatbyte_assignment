from rest_framework import serializers
from .models import PatientDoctor
from doctors.serializers import DoctorSerializer

class PatientDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientDoctor
        fields = ("id", "patient", "doctor", "created_at")
        read_only_fields = ("id", "created_at")

class DoctorsForPatientSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(read_only=True)

    class Meta:
        model = PatientDoctor
        fields = ("id", "doctor", "created_at")