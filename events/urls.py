from django.contrib import admin
from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('list/<year>/',views.EventView.as_view(),name="events_list"),
    path('noticeboard/',views.NoticeBoardListView.as_view(),name="notices_list"),
    path('register/<int:id>/', csrf_exempt(views.event_register), name='eventregister'),
    path('unregister/<int:id>/', csrf_exempt(views.event_unregister), name='eventunregister'),
]