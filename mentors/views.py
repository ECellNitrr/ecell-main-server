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

    def get(self, request, year):
        try:
            queryset = Mentor.objects.filter(year=year, flag=True)
        except:
            return Response(responses.mentors_not_found_404, status.HTTP_404_NOT_FOUND)
        else:
            serializer = MentorListSerializer(queryset, many=True)
            data = serializer.data
            return Response({"message": "Mentors Fetched successfully.", "data": data}, status.HTTP_200_OK)
