from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import JsonResponse
from django.http import Http404

from django.core.exceptions import ValidationError

from django.views.generic import View

from .forms import *
from .models import *

class Profile(LoginRequiredMixin, View):
    def get(self, request):
        createRoom_form = CreateRoomForm
        skills = UserSkill.objects.filter(user=request.user.userprofile)
        context = {
            'createRoom_form': createRoom_form,
            'skills': skills
            }
        return render(request, 'profiles/profile.html', context=context)

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
        
        skill_categories = RoomCategorySkill.objects.filter(room=room)
        # print('aaaaaaaaaaaaaaa->>>>', skill_categories)
        skills = list()
        for category in skill_categories:
            skills.append( [ skill for skill in Skill.objects.filter(category=category.category_skill) ] )

        context = {
            'room': room,
            'members':members,
            'room_admin': room_admin,
            'skill_categories': skill_categories,
            'skills': skills
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
    def get(self, request, slug):
        cur_room = Room.objects.get(slug=slug)
        msRoomUser = RoomUser.objects.filter(room=cur_room)
        members = [user.user for user in msRoomUser]
        if not members.count(request.user):
            raise Http404
        for m in msRoomUser:
            if m.is_admin:
                room_admin = m.user
        if room_admin != request.user:
            raise Http404

        category_skill = CategorySkill.objects.all()
        
        # room_skills = RoomCategorySkill.objects.filter(room=cur_room) # skills belong to current room

        category_form = CategorySkillForm
        existing_categories = RoomCategorySkill.objects.filter(room=cur_room).filter(is_active=True)
        # print(room_skills)
        context = {
            'category_skill': category_skill,
            'category_form': category_form,
            'existing_categories': existing_categories,
            'members':members,
            'cur_room': cur_room
        }

        return render(request, 'profiles/room_settings.html', context=context)
    def post(self, request, slug):
        category_skill = CategorySkill.objects.all()
        print(category_skill)
        cur_room = Room.objects.get(slug=slug)
        room_skills = RoomCategorySkill.objects.filter(room=cur_room)
        msRoomUser = RoomUser.objects.filter(room=cur_room)
        members = [user.user for user in msRoomUser]
        if not members.count(request.user):
            raise Http404
        category_form = CategorySkillForm(request.POST)
        if category_form.is_valid():
            category=category_form.cleaned_data.get('category')
            print('->>>', RoomCategorySkill.objects.filter(room=cur_room))
            if not [ x.category_skill for x in RoomCategorySkill.objects.filter(room=cur_room)].count(category):
                new_relation = RoomCategorySkill(room=cur_room, category_skill=category)
                print(new_relation.category_skill)
                new_relation.save()
            else:
                category_form.add_error('category','Error')

        existing_categories = RoomCategorySkill.objects.filter(room=cur_room)
    
        context = {
            'category_skill': category_skill,
            'category_form': category_form,
            'existing_categories': existing_categories,
            'members':members,
            'cur_room': cur_room
        }
        return render(request, 'profiles/room_settings.html', context=context)

def calc_skill(request, slug):
    skill = request.POST.get('skill')
    score = float(request.POST.get('score'))
    member = request.POST.get('member')
    user = get_object_or_404(User, username=member)
    skill_obj = get_object_or_404(Skill, name=skill)
    cur_user_score = 5.0
    for x in UserSkill.objects.filter(user=request.user.userprofile):
        if x.skill.name == skill:
            cur_user_score = float(x.value)*0.1
    sid = 0
    user_score = 0.0
    if user != request.user:
        if not [ x.skill for x in UserSkill.objects.filter(user=user.userprofile) ].count(skill_obj) :
            print('True', score*cur_user_score)
            new_relation = UserSkill(user=user.userprofile, skill=skill_obj, value=(score*cur_user_score))
            new_relation.save()
        else:
            
            for x in UserSkill.objects.filter(user=user.userprofile):
                if x.skill == skill_obj:
                    sid = x.id
                    user_score = float(x.value)
            print('Flase', 1*cur_user_score)
            if score > user_score:
                print('+++++')
                user_score += 1*cur_user_score
            else:
                print('----')
                user_score -= 1*cur_user_score

            print(request.user, user, cur_user_score, score, user_score)
            new_history = History(
                who_vote=request.user, 
                for_whom_vote=user, 
                coefficient_who_vote=cur_user_score, 
                mark_who_vote=score,
                value_for_whom_vote= user_score
                )
            new_history.save()
            UserSkill.objects.filter(id=sid).update(value=user_score)

    print(skill, score, member, user_score)
    return redirect(Room.get_redirect_url(slug=slug))

def delete_category(request, slug):
    categories = request.POST.getlist('delete_category')
    print(categories)
    cur_room = get_object_or_404(Room, slug=slug)
    for category in categories:
        print(category)
        cur_category = get_object_or_404(CategorySkill, name=category)
        print('cur_category', cur_category)
        print('Before delete', RoomCategorySkill.objects.filter(room=cur_room).filter(category_skill=cur_category) )
        instance  = RoomCategorySkill.objects.filter(room=cur_room).filter(category_skill=cur_category)
        instance.delete()
        print('asdasd', instance)
        print('After delete', RoomCategorySkill.objects.filter(room=cur_room).filter(category_skill=cur_category))

    return redirect(Room.get_settings_url(slug=slug))
