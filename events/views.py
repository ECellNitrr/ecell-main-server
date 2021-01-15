from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from .models import Event, EventRegister
from .serializers import *
from decorators import ecell_user
from rest_framework import status, generics
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny,IsAuthenticated
from utils.swagger import set_example
from rest_framework.views import APIView
from . import responses

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
            try:
                registeredUser = EventRegister.objects.get(user=user,event=event)
            except:
                eventregister.user = user
                eventregister.event = event
                eventregister.save()
                return Response(responses.event_registration_201,status.HTTP_201_CREATED)
            return Response(responses.user_already_registered_event_200,status.HTTP_200_OK)    
        else:
            return Response(responses.user_unauthorized_401,status.HTTP_401_UNAUTHORIZED)

# TODO: simplify with drf
@api_view(['POST', ])
@ecell_user
def event_unregister(request, id):
    u = request.ecelluser
    if u:
        try:
            e = Event.objects.get(id=id)
        except:
            res_message="Event does not exist"
            res_status=status.HTTP_404_NOT_FOUND   
        else:
            try:
                reg = EventRegister.objects.filter(user = u, event= e)  
            except:
                res_message= "Event not registered"
                res_status=status.HTTP_404_NOT_FOUND
            else:
                res_message="Registration deleted successfully"
                reg.delete()
                res_status=status.HTTP_200_OK
    
    else:
        res_message = "Login to continue"
    return Response({
        "message": res_message
    }, status=res_status)


# TODO: in next meeting report why this exsits
class NoticeBoardListView(ListAPIView):
    queryset = NoticeBoard.objects.filter(show=True)
    serializer_class = NoticeBoardSerializer