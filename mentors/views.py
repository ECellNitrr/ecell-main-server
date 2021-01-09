# TODO: remove unused imports
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from .models import Mentor
from .serializers import MentorSerializer, MentorListSerializer
from decorators import ecell_user
from django.http import HttpResponse
import csv


# TODO: simplify with drf
@api_view(['GET', ])
def get_mentors(request, year):

    res_message = ""
    res_status = ""
    res_data = []

    mentors = Mentor.objects.filter(year=year, flag=True)
    if len(mentors) > 0:
        res_data = MentorListSerializer(
            mentors, many=True, context={
                'request': request}).data
        res_message = "Mentors Fetched successfully."
        res_status = status.HTTP_200_OK
    else:
        res_message = "Mentors Couldn't be fetched"
        res_status = status.HTTP_404_NOT_FOUND

    return Response({
        "message": res_message,
        "data": res_data
    }, status=res_status)
