from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def tutor_profile(request):
    return render(request, 'userprofile/tutor_profile.html')


def man_home(request):
    return render(request, 'man/index.html')