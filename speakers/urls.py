from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('full_list/', views.get_speakers_list),
]
