from django.shortcuts import render, redirect
from django.views.generic import View


from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)

from .forms import UserLoginForm, UserSignupForm

from profiles.models import UserProfile

def login_view(request):
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('/')

    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context=context)

def signup_view(request):
    next = request.GET.get('next')
    form = UserSignupForm(request.POST or None)
    if form.is_valid() :
        if form.cleaned_data.get('password') != form.cleaned_data.get('password_confirm'):
            form.add_error('password','Пароль не совпадает')
        else:
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            userprofile = UserProfile.objects.create(user=user)
            new_user = authenticate(username=user.username, password=password)

            login(request, new_user)
            if next:
                return redirect(next)
            return redirect('/')

    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context=context)
            
def logout_view(request):
    logout(request)
    return redirect('/')