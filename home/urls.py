from django.urls import path

from .views import home, room

urlpatterns = [
    path('', home),
    path('room/', room, name='room_url')
]
