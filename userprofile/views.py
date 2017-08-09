from django.shortcuts import render

# Create your views here.


def man_home(request):
    return render(request, 'man/index.html')