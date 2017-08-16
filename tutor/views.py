from django.shortcuts import render

# Create your views here.
def tutor_list(request):
    return render(request, 'tutor/tutor_list.html')