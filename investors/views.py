from rest_framework.viewsets import ModelViewSet
from .models import Investor
from .serializers import InvestorSerializer
from django_filters import rest_framework as filters


class FullInvestorsAPIView(ModelViewSet):
    queryset = Investor.objects.all()
    serializer_class = InvestorSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('year',)


