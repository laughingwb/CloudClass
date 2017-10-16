from django.shortcuts import render
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext
from django.contrib.auth.models import User
from .models  import UserDetail
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout,login
from django.shortcuts import render, redirect
from django.shortcuts import render,render_to_response
from tutor.utils import is_tutor
from django.http import HttpResponseRedirect

# Create your views here.
import jpush
from jpush import common

def signup(request):
    return render(request, 'account/signup.html')

def loginhtml(request):
    _jpush = jpush.JPush(u'47cd8c54b7d852e01ffb82ac', u'5838452a357f53a742fb509d')
    _jpush.set_logging("DEBUG")

    push = _jpush.create_push()
    push.audience = jpush.all_
    push.notification = jpush.notification(alert="!hello python jpush api")
    push.platform = jpush.all_
    try:
        response = push.send()
        print("send")
    except common.Unauthorized:
        print("Unauthorized")
        raise common.Unauthorized("Unauthorized")
    except common.APIConnectionException:
        raise common.APIConnectionException("conn")
    except common.JPushFailure:
        print("JPushFailure")
    except:
        print("Exception")

    return render(request, 'account/login.html')

def loginAccount(request):


    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    print(username)
    print(password)
    loginuser = authenticate(username=username, password=password)
    if loginuser is not None:
        # the password verified for the user
        if loginuser.is_active:
            print("User is valid, active and authenticated")
            login(request, loginuser)
        else:
            print("The password is valid, but the account has been disabled!")
            return render(request, "account/login.html", {'code': '1'})
    else:
        print("The username and password were incorrect.")
        return render(request, "account/login.html", {'code': '2'})
        # the authentication system was unable to verify the username and password

    if is_tutor(request.user):
        # return redirect('scheduler.views.entry_tutor')
        return redirect('userprofile.views.tutor_profile')
    else:
        return redirect('userprofile.views.profile')


@login_required
def logouthtml(request):
    return render(request, 'account/logout.html')

def logoutAccount(request):
    print(request.user.username + ' Logout')
    logout(request)
    return render(request, 'userprofile/profile.html')

def signupAccount(request):
    username = request.POST.get('username', '')
    email = request.POST.get('email', '')
    password = request.POST.get('password1', '')
    print(password)
    try:
        user = User.objects.get(username=username)
        return render(request, 'account/signup.html')
    except ObjectDoesNotExist:
        user = User.objects.create_user(username, email, password)
        user.save()
        userInfo = UserDetail.objects.create(user=user)
        loginuser = authenticate(username=username, password=password)
        if loginuser is not None:
            # the password verified for the user
            if loginuser.is_active:
                print("User is valid, active and authenticated")
                login(request, loginuser)
                return redirect('userprofile.views.profile')
            else:
                print("The password is valid, but the account has been disabled!")
                return render(request, "account/login.html", {'code': '1'})
        else:
            print("The username and password were incorrect.")
            return render(request, "account/login.html", {'code': '2'})
    return render(request, 'userprofile/profile.html')

