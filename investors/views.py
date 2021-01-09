# TODO: delete unused imports
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from .models import Investor
from .serializers import InvestorSerializer
from decorators import ecell_user
from django.http import HttpResponse, JsonResponse
from django_filters import rest_framework as filters


class FullInvestorsAPIView(ModelViewSet):
    queryset = Investor.objects.all()
    serializer_class = InvestorSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('year',)
