from django.shortcuts import render
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from .models  import UserInfo
# Create your views here.


def signup(request):
    return render(request, 'account/signup.html')

def login(request):
    return render(request, 'account/login.html')

def loginAccount(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    print(username)
    user = authenticate(username=username, password=password)
    if user is not None:
        # the password verified for the user
        if user.is_active:
            print("User is valid, active and authenticated")
            return render(request, 'userprofile/profile.html')
        else:
            print("The password is valid, but the account has been disabled!")
            return render(request, "account/login.html", {'code': '1'})
    else:
        print("The username and password were incorrect.")
        return render(request, "account/login.html", {'code': '2'})
        # the authentication system was unable to verify the username and password

    return render(request, 'userprofile/profile.html')

def signupAccount(request):
    username = request.POST.get('username', '')
    email = request.POST.get('email', '')
    password = request.POST.get('password1', '')
    try:
        user = User.objects.get(username=username)
        return render(request, 'account/signup.html')
    except ObjectDoesNotExist:
        user = User.objects.create_user(username, email, password)
        user.save()
        userInfo = UserInfo.objects.create(username = username)

    return render(request, 'userprofile/profile.html')