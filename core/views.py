from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from utils.swagger import set_example
from . import responses
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
# Create your views here.

class AuthCheckView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_id="check_auth",
        responses = {
            '200' : set_example(responses.user_authenticated_200),
            '401' : set_example(responses.user_unauthorized_401)
        }
    )
    def get(self,request):
        return Response(responses.user_authenticated_200,status.HTTP_200_OK)