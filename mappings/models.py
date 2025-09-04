from django.db import models
from patients.models import Patient
from doctors.models import Doctor

class PatientDoctor(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="patient_doctors")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="doctor_patients")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("patient", "doctor")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.patient.name} -> {self.doctor.name}"
