from django.shortcuts import render
from django.shortcuts import render, redirect
from tutor.utils import is_tutor
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def entry(request):
    if is_tutor(request.user):
        return redirect('scheduler.views.entry_tutor')

    return render(request, 'scheduler/entry.html')

@login_required
def entry_tutor(request):
    return render(request, 'scheduler/entry_tutor.html')

@login_required
def calendar(request):
    return  render(request, 'scheduler/calendar.html')