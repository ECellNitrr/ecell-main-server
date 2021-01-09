# TODO: remove unwnted imports
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from .models import Speaker
from .serializers import SpeakerSerializer, SpeakerListSerializer
from decorators import ecell_user
from django.http import HttpResponse, JsonResponse
import csv


@api_view(['GET', ])
def get_speakers_list(request):
    speakers_objs = Speaker.objects.all()
    speakers = SpeakerSerializer(speakers_objs, many=True).data
    return JsonResponse(speakers,safe=False)
