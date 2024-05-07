from rest_framework.response import Response
from docutils.nodes import status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .serializers import *
from med.models import *


class ProfileUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserEditSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self):
        return self.request.user


class GetMeView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class SpecialityListView(generics.ListAPIView):
    queryset = Speciality.objects.all()
    serializer_class = SpeicalitySerializer


class HospitalizationView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Hospitalization.objects.all()
    serializer_class = HospitalizationSerializer

    def create(self, request, *args, **kwargs):
        patient_data = request.data.pop('patient')
        passport_data = request.data.pop('passport')

        patient_serializer = UserSerializer(data=patient_data)
        if not patient_serializer.is_valid():
            return Response(patient_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        patient = patient_serializer.save()

        passport_serializer = PassportSerializer(data=passport_data)
        if not passport_serializer.is_valid():
            return Response(passport_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        passport = passport_serializer.save(patient=patient)

        request.data['patient'] = patient.id
        request.data['passport'] = passport.id

        hospitalization_serializer = self.get_serializer(request.data)
        hospitalization_serializer.is_valid(raise_exception=True)
        self.perform_create(hospitalization_serializer)

        headers = self.get_success_headers(hospitalization_serializer)
        return Response(HospitalizationSerializer(hospitalization_serializer).data, status=status.HTTP_201_CREATED, headers=headers)





