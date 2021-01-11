from django.contrib import admin
from django.urls import path
from .models import Mentor
from . import views
from .serializers import MentorListSerializer

urlpatterns = [
    path('list/<year>', views.MentorView.as_view(), name='mentor_list')
]
