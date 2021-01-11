from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from utils.swagger import set_example
from .models import Mentor
from .serializers import MentorListSerializer
from rest_framework import status, generics
from . import responses


class MentorView(generics.ListAPIView):
    permission_classes = [AllowAny, ]
    queryset = Mentor.objects.all()
    serializer_class = MentorListSerializer

    @swagger_auto_schema(
        operation_id='get_mentors',
        responses={
            '200': set_example(responses.get_mentors_200),
            '404': set_example(responses.mentors_not_found_404),
        },
    )
    def list(self, request, year):
        queryset = Mentor.objects.filter(year=year, flag=True)
        serializer = MentorListSerializer(queryset, many=True)
        data = serializer.data
        if queryset.count() > 0:
            return Response({"message": "Mentors Fetched successfully.", "data": data}, status.HTTP_200_OK)
        else:
            return Response({"message": "Mentors Couldn't be fetched"}, status.HTTP_404_NOT_FOUND)
