from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from .models import Mentor
from .serializers import MentorSerializer, MentorListSerializer
from decorators import ecell_user
from django.http import HttpResponse
import csv
from rest_framework import status, generics, filters

class MentorView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Mentor.objects.all()
    serializer_class = MentorListSerializer

    def list(self, request, year):
        queryset = Mentor.objects.filter(year=year, flag=True)
        serializer = MentorListSerializer(queryset, many=True)
        data = serializer.data
        if queryset.count() > 0:
            return Response({"message":"Mentors Fetched successfully.", "data":data}, status.HTTP_200_OK)
        else:
            return Response({"message":"Mentors Couldn't be fetched"}, status.HTTP_404_NOT_FOUND)
