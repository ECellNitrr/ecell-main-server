from django.contrib import admin
from django.urls import path
from . import views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('', views.FullInvestorsAPIView)


urlpatterns = [
]

urlpatterns += router.urls