from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import JsonResponse
from django.http import Http404

from django.core.exceptions import ValidationError

from django.views.generic import View

from .forms import EditUserProfileForm, CreateRoomForm, AddRoomMemberForm
from .models import UserProfile, Room, RoomUser

@login_required(login_url='login_url')
def profile(request):
    return render(request, 'profiles/profile.html', context={})

class Profile(LoginRequiredMixin, View):
    def get(self, request):
        createRoom_form = CreateRoomForm
        return render(request, 'profiles/profile.html', context={'createRoom_form': createRoom_form})

@login_required(login_url='login_url')
def edit_profile(request):
    form = EditUserProfileForm(request.POST or None)

    if request.method == 'POST':
        userprofile = UserProfile.objects.get(user=request.user)

        if form.is_valid():

            avatar = request.POST
            print(avatar)
    return render(request, 'profiles/edit_profile.html', context={'form': form})

class EditProfile(LoginRequiredMixin, View):
    def get(self, request):
        userProfile = UserProfile.objects.get(user=request.user)
        form = EditUserProfileForm(instance=userProfile)
        return render(request, 'profiles/edit_profile.html', context={'form': form})
    
    def post(self, request):
        userProfile = UserProfile.objects.get(user=request.user)
        form = EditUserProfileForm(request.POST, request.FILES, instance=userProfile)
        
        if form.is_valid():
            print(request.POST)
            new_userProfile = form.save()
            return redirect('profile_url')
        return render(request, 'profiles/edit_profile.html', context={'form': form}) 

class RoomDetail(LoginRequiredMixin, View):
    def get(self, request, slug):
        room = get_object_or_404(Room, slug__iexact=slug)
        msRoomUser = RoomUser.objects.filter(room=room)
        members = [user.user for user in msRoomUser]
        if not members.count(request.user):
            raise Http404
        for m in msRoomUser:
            if m.is_admin:
                room_admin = m.user
        context = {
            'room': room,
            'members':members,
            'room_admin': room_admin
        }

        return render(request, 'profiles/room_detail.html', context=context)
    def post(self, request, slug):
        room = get_object_or_404(Room, slug__iexact=slug)
        msRoomUser = RoomUser.objects.filter(room=room)
        members = [user.user for user in msRoomUser]
        if not members.count(request.user):
            raise Http404
        for m in msRoomUser:
            if m.is_admin:
                room_admin = m.user

        search_user = request.POST.get('search', '')
        user_add = User.objects.get(username=search_user)
        if search_user and not members.count(user_add):
            RoomUser.objects.create(user=user_add, room=room)
            members.append(user_add)
        context = {
            'room': room,
            'members':members,
            'room_admin': room_admin
        }
        return render(request, 'profiles/room_detail.html', context=context)

class RoomCreate(LoginRequiredMixin, View):
    def get(self, request):
        form = CreateRoomForm
        return render(request, 'profiles/room_create.html', context={'form': form})
    def post(self, request):
        bound_form = CreateRoomForm(request.POST)
        if bound_form.is_valid():
            new_room = bound_form.save()
            m1 = RoomUser(room=new_room, user=request.user, is_admin=True)
            m1.save()
            return redirect('/')
        return render(request, '/', {'createRoom_form': bound_form})


@login_required(login_url='login_url')
def search_users(request):
    search_user = request.GET.get('username', '')
    print('ajax', search_user)
    qs_user = User.objects.filter(username__iexact=search_user).all()
    data = {}
    if qs_user:
        data = {
            'username': qs_user[0].username,
            'avatar_url': qs_user[0].userprofile.avatar.url
        }
    print('Data', data)
    return JsonResponse(data)

class RoomSettings(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'profiles/room_settings.html', context={})