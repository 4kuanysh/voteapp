from django.urls import path

from .views import login_view, register_view, logout_view

urlpatterns = [
    path('login/', login_view, name='login_url'),
    path('register/', register_view, name='register_url'),
    path('logout/', logout_view, name='logout_url'),
]
