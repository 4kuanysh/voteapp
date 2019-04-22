from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, 'home/profile.html', {})

@login_required
def room(request):
    return render(request, 'home/vote.html', {})
# def home(request):
#     if request.user.is_authenticated:
#         return render(request, 'home/home.html', {})
#     return redirect(reverse('login_url'))