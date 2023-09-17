from django.shortcuts import render
from django.urls import URLResolver

from basic_app.froms import UserCreationForm, UserProfileInfoForm

# Create your views here.
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('Account not active')
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(
                username, password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'basic_app/login.html', {})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
def special(request):
    return HttpResponse("You are logged in, Nice!")


def index(request):
    return render(request, 'basic_app/index.html')


def register(request):
    register = False
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        profile_form = UserProfileInfoForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            register = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserCreationForm()
        profile_form = UserProfileInfoForm()
    return render(request, 'basic_app/registration.html', {'user_form': user_form, 'profile_form': profile_form, 'register': register})
