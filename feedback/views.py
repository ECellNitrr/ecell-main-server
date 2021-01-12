from utils.swagger import set_example
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import FeedbackSerializer
from rest_framework import serializers, status
from . import responses
class FeedbackView(APIView):
    @swagger_auto_schema(
        request_body=FeedbackSerializer,
        responses={
            '201' : set_example(responses.feedback_created_201),
            '400' : set_example(responses.feedback_invalid_400)
        }
    )
    def post(self,request):
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(responses.feedback_created_201,status.HTTP_201_CREATED)
        else:
            error = serializer.errors
            error_msg = ""
            for err in error:
                error_msg += "Error in field: "+str(err)+"- "+str(error[err][0]) + " "
            return Response({"message" : error_msg},status.HTTP_400_BAD_REQUEST)

