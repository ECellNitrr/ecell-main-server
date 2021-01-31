from django.urls import path
from . import views

urlpatterns = [
    path('check_auth/', views.AuthCheckView.as_view(), name="check_auth"),
]
