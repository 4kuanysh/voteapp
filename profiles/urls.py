from django.urls import path
from .views import profile, edit_profile, EditProfile, RoomDetail, RoomCreate, Profile, search_users

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', Profile.as_view(), name='profile_url'),
    path('profile/edit/', EditProfile.as_view(), name='edit_profile_url'),
    path('ajax/searchuser/', search_users, name='search_user_ajax'),
    path('room/<str:slug>/', RoomDetail.as_view(), name='room_detail_url'),
    path('room/create', RoomCreate.as_view(), name='create_room_url')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)