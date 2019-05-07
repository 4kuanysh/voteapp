from django import forms
from django.contrib.auth.models import User

from .models import *


class EditUserProfileForm(forms.ModelForm):
    avatar = forms.ImageField(label=('Avatar'),required=False, error_messages = {'invalid':("Image files only")}, widget=forms.FileInput)
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

class CategorySkillForm(forms.Form):
    category = forms.ModelChoiceField( 
        queryset=CategorySkill.objects.all().order_by('name'), 
        widget=forms.Select(attrs={'class': 'form-control'}) 
    )

    
    

        