from utils.swagger import set_example
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import FeedbackSerializer
from rest_framework import status
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
        f = FeedbackSerializer(data=request.data)
        if f.is_valid():
            f.save()
            return Response({"message" : "Feedback Posted Successfully"},status.HTTP_201_CREATED)
        else:
            error = f.errors
            error_msg = ""
            for err in error:
                error_msg += "Error in field: "+str(err)+"- "+str(error[err][0]) + " "
            return Response({"message" : error_msg},status.HTTP_400_BAD_REQUEST)

