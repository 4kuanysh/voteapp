from django import forms
from django.contrib.auth.models import User

from .models import UserProfile, Room


class EditUserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'avatar'
        ]

class CreateRoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = [
            'name'
        ]

class AddRoomMemberForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username'
        ]

    
    

        