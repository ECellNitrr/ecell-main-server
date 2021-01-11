from django.urls import path
from . import views

urlpatterns = [
    path('list/<year>/', views.MentorView.as_view(), name='mentor_list')
]
