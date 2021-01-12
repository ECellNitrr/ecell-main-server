from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from .models import Event, EventRegister
from .serializers import *
from decorators import ecell_user
from rest_framework import status, generics
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from utils.swagger import set_example
from . import responses

class EventView(generics.ListAPIView):
    permission_classes = [AllowAny, ]
    queryset = Event.objects.all()
    serializer_class = EventListSerializer
    @swagger_auto_schema(
        operation_id='get_events',
        request_body=EventListSerializer,
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
        if queryset.count() >= 0:
            return Response({"message":"Events Fetched successfully","data":data},status.HTTP_200_OK)

# TODO: simplify with drf
@api_view(['POST', ])
@ecell_user
def event_register(request, id):
    eventregister = EventRegister()
    user = request.ecelluser
    res_status = status.HTTP_401_UNAUTHORIZED
    if user.verified:
        eventregister.user = user
        try:
            eventregister.event = Event.objects.get(id=id)
        except:
            res_message="Registration Failed. Event does not exist."
            res_status=status.HTTP_404_NOT_FOUND
            
        else:
            eventregister.save()
            res_message= "Registration Successful"
            res_status=status.HTTP_200_OK
    else:
        res_message = "You need to verify your account to register for an event"
    return Response({
        "message": res_message
    }, status=res_status)



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