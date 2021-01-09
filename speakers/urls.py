from django.contrib import admin
from django.urls import path
from . import views
from utils.speaker_trans import data_transfer

urlpatterns = [
    path('full_list/', views.get_speakers_list),
    path('data_transfer/', data_transfer)
    ]
