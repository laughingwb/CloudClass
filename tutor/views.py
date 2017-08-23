from django.shortcuts import render
from tutor.models import Teacher
# Create your views here.
def tutor_list(request):
    tutors = Teacher.objects.filter().order_by('id');
    print(tutors)
    return render(request, 'tutor/tutor_list.html', {'tutors':tutors })