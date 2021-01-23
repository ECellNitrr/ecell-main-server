from rest_framework.decorators import api_view
from .models import Speaker
from .serializers import SpeakerSerializer
from django.http import JsonResponse
from utils.swagger import set_example
from drf_yasg.utils import swagger_auto_schema
from . import responses


@swagger_auto_schema(
    operation_id='get_speakers',
    method='get',
    responses={
        '200': set_example(responses.get_speakers_200)
    }
)
@api_view(['get'])
def get_speakers_list(request):
    speakers_objs = Speaker.objects.all()
    speakers = SpeakerSerializer(speakers_objs, many=True).data
    response = {
        "message": "Speakers Fetched Successfully",
        "data": speakers
    }
    return JsonResponse(response,safe=False)
