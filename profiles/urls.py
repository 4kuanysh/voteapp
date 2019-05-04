from django.urls import path
from .views import *

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', Profile.as_view(), name='profile_url'),
    path('profile/edit/', EditProfile.as_view(), name='edit_profile_url'),
    path('ajax/searchuser/', search_users, name='search_user_ajax'),
    path('calculateion/<str:slug>/', calc_skill, name='calc_skill_url'),
    path('room/<str:slug>/settings/delete', delete_category, name='room_category_delete_url'),
    path('room/<str:slug>/settings/', RoomSettings.as_view(), name='room_settings_url'),
    path('room/<str:slug>/', RoomDetail.as_view(), name='room_detail_url'),
    path('room/create', RoomCreate.as_view(), name='create_room_url')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)