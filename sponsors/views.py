# TODO: remove unused
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from .models import Sponsor, spons_types
from .serializers import SponsorSerializer, SponsorListSerializer
from decorators import ecell_user
from django.http import HttpResponse, JsonResponse
from collections import defaultdict
import csv


@api_view(['GET', ])
def get_sorted_sponsors(request, year):
    sponsors_objs = Sponsor.objects.filter(flag=True, year=year)

    spons_categories = []
    res_data = {}
    Error = 'No Error'
    try:
        for x in spons_types:
            display_name = spons_types[x]['display_name']
            res_data[display_name] = list(sorted(
                [x for x in sponsors_objs.filter(spons_type=x)], 
                key=lambda x: x.importance, 
                reverse=True
                ))
            res_data[display_name] = [SponsorListSerializer(x).data for x in res_data[display_name]]
            if not res_data[display_name]:
                res_data.pop(display_name)
            else: 
                spons_categories.append(display_name)
    except Exception as e:
        Error = f"Error is: {e}"
        pass 


    return Response({
        "data": res_data,
        'message': 'fetched successfully',
        'spons_categories': spons_categories,
        'Error': Error
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny,])
def spons_years(request):
    spons_years = Sponsor.objects.values_list('year',flat=True).distinct()
    spons_years = [x for x in spons_years]
    spons_years.sort()
    return JsonResponse({'spons_year': spons_years})