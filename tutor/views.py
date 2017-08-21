from django.shortcuts import render
from tutor.models import Tutor
# Create your views here.
def tutor_list(request):
    tutors = Tutor.objects.filter().order_by('id');
    print(tutors)
    return render(request, 'tutor/tutor_list.html',{'tutors':tutors })