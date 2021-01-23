from rest_framework.decorators import  permission_classes
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from .models import Event, EventRegister
from .serializers import *
from drf_yasg.utils import swagger_auto_schema
<<<<<<< HEAD
from rest_framework.permissions import AllowAny,IsAuthenticated
=======
>>>>>>> e8bf5e4fb5d6e7d738b44ee190246ab4c2b89859
from utils.swagger import set_example
from rest_framework.views import APIView
from . import responses
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework import status, generics

class EventView(generics.ListAPIView):
    permission_classes = [AllowAny, ]
    queryset = Event.objects.all()
    serializer_class = EventListSerializer
    @swagger_auto_schema(
        operation_id='get_events',
        responses={
            '200': set_example(responses.get_events_200),
            '404': set_example(responses.events_not_found_404),
        },
    )
    def get(self,request,year):
        try:
            queryset = Event.objects.filter(year=year, flag=True)
        except:
            return Response(responses.events_not_found_404, status.HTTP_404_NOT_FOUND)
        serializer = EventListSerializer(queryset, many=True, context={'request': request})
        data = serializer.data
        return Response({"message":"Events Fetched successfully","data":data},status.HTTP_200_OK)


class EventRegisterView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_id="event_register",
        responses = {
            '201': set_example(responses.event_registration_201),
            '200':set_example(responses.user_already_registered_event_200),
            '404':set_example(responses.event_does_not_exist_404),
            '401':set_example(responses.user_unauthorized_401)
        }
    )
    def post(self,request,id):
        user = request.user
        eventregister = EventRegister()
        try:
            event = Event.objects.get(id=id)
        except:
            return Response(responses.event_does_not_exist_404, status.HTTP_404_NOT_FOUND)

        if user.verified:
            #Checking if user is already registered
            try:
                EventRegister.objects.get(user=user,event=event)
            except:
                #Registering the user if not registered
                eventregister.user = user
                eventregister.event = event
                eventregister.save()
                return Response(responses.event_registration_201,status.HTTP_201_CREATED)

            return Response(responses.user_already_registered_event_200,status.HTTP_200_OK)

        return Response(responses.user_unauthorized_401,status.HTTP_401_UNAUTHORIZED)

class EventUnregisterView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_id="eventunregister",
        responses={
            '200' : set_example(responses.event_registration_deleted_200),
            '401' : set_example(responses.user_unauthorized_401),
            '404' : set_example(responses.event_does_not_exist_404)
        }
    )
    def post(self, request, id):
        try:
            event = Event.objects.get(id=id)
        except:
            return Response(responses.event_does_not_exist_404,status.HTTP_404_NOT_FOUND) 
        else:
            try:
                reg = EventRegister.objects.get(user = request.user, event= event)  
            except:
                return Response(responses.event_not_registered_404,status.HTTP_404_NOT_FOUND)
            else:
                reg.delete()
                return Response(responses.event_registration_deleted_200,status.HTTP_200_OK)    

# TODO: in next meeting report why this exsits
class NoticeBoardListView(ListAPIView):
    queryset = NoticeBoard.objects.filter(show=True)
    serializer_class = NoticeBoardSerializer
