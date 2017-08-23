from django.shortcuts import render
import json
import datetime, pytz
import dateutil.parser
from datetime import timedelta, datetime, date
from django.shortcuts import render, redirect
from tutor.utils import is_tutor
from django.contrib.auth.decorators import login_required
from scheduler.utils import get_localized_datetime
from scheduler.utils import get_monday_of_the_week as get_monday
from scheduler.utils import get_next_monday_of_the_week as get_next_monday
from scheduler.models import Event, EventSubscription, Appointment, EventManager
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import User
from scheduler.utils import get_one_week_range
from django.http import HttpResponse
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
def delete_event(request):
    event_id = request.GET.get('event_id', '')

    if event_id == '':
        return HttpResponse(_("event id is null"))
    try:
        en = Event.objects.get(id=event_id)
        es = EventSubscription.objects.filter(event_id=event_id).first()
        if es:
            return HttpResponse(_('event has been subscribed, and it can not be deleted'))
        en.delete()
        return HttpResponse(_("event is deleted successfully"))

    except Event.DoesNotExist:
        return HttpResponse(_("event does not exist"))

@login_required
def event(request):
    user = request.GET.get('user')
    userobject = User.objects.get(id=user)

    d, t_monday, t_next_monday = get_one_week_range(request.GET.get('date'), None, request.GET.get('action'))
    # result will be filtered by start_date and end_date
    occurrences = EventManager.get_occurrence_list(user, t_monday, t_next_monday)

    # logger.debug(occurrences)

    msg = request.GET.get("msg")
    return render(request, 'scheduler/event.html',
                  {'occurrences': json.dumps([o.__dict__ for o in occurrences], cls=DjangoJSONEncoder), 'date': d,
                   'user': user, 'msg': msg, 'userobject':userobject})

def scheduler_publish(request):
    date = request.POST.get('date')
    end_recurring_period = request.POST.get('end_recurring_period')
    e_id = request.POST.get('event_id')
    e_start = request.POST.get('event_start')
    e_end = request.POST.get('event_end')

    t_end_recurring_period = get_localized_datetime(end_recurring_period)

    t_end_recurring_period = t_end_recurring_period + timedelta(days=1)

    if e_id:
        event_update = Event.objects.get(id=e_id)
        event_update.end_recurring_period = t_end_recurring_period
        event_update.save()
    else:
        user = User.objects.get(id=request.user.id)
        event_add = Event(user=user,
                          start=e_start,
                          end=e_end,
                          end_recurring_period=t_end_recurring_period, )
        event_add.save()

    return redirect('/scheduler/calendar/',date=date)

@login_required
def subscribe(request):
    d = request.POST.get('date')
    user = request.POST.get('user')
    return redirect('/scheduler/event/?user=' + user, date=d)

@login_required
def calendar(request):
    user = request.user.id
    d = request.GET.get('date')
    if d is None:
        today = date.today()
        d = today.strftime('%Y-%m-%d');
    t_datetime = get_localized_datetime(d)

    action = request.GET.get('action')
    if action:
        if action == 'previous':
            t_datetime = t_datetime - timedelta(days=7)
        elif action == 'next':
            t_datetime = t_datetime + timedelta(days=7)

    d = t_datetime.strftime('%Y-%m-%d')
    occurrences = EventManager.get_occurrence_list(user, get_monday(t_datetime), get_next_monday(t_datetime))
    print(occurrences)

    return render(request, 'scheduler/calendar.html',
                  {'occurrences': json.dumps([o.__dict__ for o in occurrences], cls=DjangoJSONEncoder), 'date': d,
                   'event_duration': Event.default_event_duration,
                   })