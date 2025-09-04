from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import PatientDoctor
from .serializers import PatientDoctorSerializer, DoctorsForPatientSerializer
from patients.models import Patient

class MappingPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj: PatientDoctor):
        # Only allow delete if the mapping belongs to a patient owned by the user
        return obj.patient.created_by_id == request.user.id

class MappingViewSet(viewsets.ModelViewSet):
    queryset = PatientDoctor.objects.select_related("patient", "doctor")
    serializer_class = PatientDoctorSerializer
    permission_classes = [MappingPermission]

    def get_queryset(self):
        # Users can only see mappings for their own patients
        return PatientDoctor.objects.select_related("patient", "doctor").filter(
            patient__created_by=self.request.user
        )

    def perform_create(self, serializer):
        patient = serializer.validated_data.get("patient")
        if patient.created_by_id != self.request.user.id:
            raise PermissionDenied("You can only map doctors for your own patients.")
        serializer.save()

    @action(detail=False, methods=["get"], url_path=r"patient/(?P<patient_id>\d+)")
    def doctors_for_patient(self, request, patient_id=None):
        try:
            patient = Patient.objects.get(id=patient_id, created_by=request.user)
        except Patient.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        qs = PatientDoctor.objects.select_related("doctor").filter(patient=patient)
        data = DoctorsForPatientSerializer(qs, many=True).data
        return Response(data, status=status.HTTP_200_OK)
