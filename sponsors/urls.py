from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('sorted_list/<int:year>/', views.get_sorted_sponsors, name="get_sponsors"),
    path('spons_years/', views.spons_years)
]