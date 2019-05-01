from django.urls import path
from .views import login_view, signup_view, logout_view

urlpatterns = [
    path('login/', login_view, name='login_url'),
    path('signup/', signup_view, name='signup_url'),
    path('logout/', logout_view, name='logout_url'),
]