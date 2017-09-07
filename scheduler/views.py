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
from django.contrib import messages
from django.utils.translation import ugettext as _
from virtualclass.models import VirtualClass
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
    quick_appointment = True if request.POST.get('quick_appointment', '0') == '1' else False
    e_id = request.POST.get('event_id')
    s_id = request.POST.get('subscription_id')
    s_start_date = request.POST.get('subscription_start')
    s_end_date = request.POST.get('subscription_end')
    if not s_start_date or s_start_date == "":
        return redirect('/scheduler/event/?user=' + user, date=d)
    if not s_end_date or s_end_date == "":
        return redirect('/scheduler/event/?user=' + user, date=d)

    if not quick_appointment and (s_start_date == '' or s_end_date == ''):
        messages.add_message(request, messages.WARNING, _("start date and end date is mandatory input"))
        return redirect('/scheduler/event/?user=' + user, date=d)

    if quick_appointment:
        t_s_start = get_localized_datetime(request.POST.get('current_dt'))
        #t_s_end = t_s_start + timedelta(days=1)
    else:
        t_s_start = get_localized_datetime(s_start_date)
        t_s_end = get_localized_datetime(s_end_date)
        if t_s_end:
            t_s_end = t_s_end + timedelta(days=1)
        else:
            messages.add_message(request, messages.WARNING, _('Subscription end date is not valid date') )
            return redirect('/scheduler/event/?user=' + user, date=d)

    try:
        event = Event.objects.get(id=e_id)

        if quick_appointment:
            a_duration = event.end - event.start
            t_s_end = t_s_start + a_duration

        if event.end_recurring_period < t_s_end or get_localized_datetime(event.start).date() > t_s_start.date():
            messages.add_message(request, messages.WARNING,
                                 _('Subscription date range mismatches with event date range'))
            return redirect('/scheduler/event/?user=' + user, date=d)
    except Event.DoesNotExist:
        messages.add_message(request, messages.WARNING, _('Event does not exist') )
        return redirect('/scheduler/event/?user=' + user, date=d)

    conflict_exists, conflict_sub = EventManager.check_subscription_conflict(user, event, t_s_start, t_s_end, s_id)

    if conflict_exists:
        messages.add_message(request, messages.WARNING, _("A time conflict exists with subscription, from {} to {}, by {}".format(
            conflict_sub.start_time.strftime('%Y-%m-%d'), conflict_sub.end_time.strftime('%Y-%m-%d'), conflict_sub.invitee.username) ) )
        return redirect('/scheduler/event/?user=' + user, date=d)
    conflict_exists, conflict_sub = EventManager.check_subscription_conflict(request.user.id, event, t_s_start, t_s_end,
                                                                             s_id)
    if conflict_exists:
        messages.add_message(request, messages.WARNING,
                             _("A time conflict exists with subscription, from {} to {}, by {}".format(
                                 conflict_sub.start_time.strftime('%Y-%m-%d'),
                                 conflict_sub.end_time.strftime('%Y-%m-%d'), conflict_sub.invitee.username)))
        return redirect('/scheduler/event/?user=' + user, date=d)

    if s_id:
        s_update = EventSubscription.objects.get(id = s_id)
        s_update.start_time = t_s_start
        s_update.end_time = t_s_end
        s_update.save()
    else:
        s_user = request.user
        s_event = Event.objects.get(id=e_id)
        s_add = EventSubscription(invitee=s_user,
                                  event=s_event,
                                  start_time=t_s_start,
                                  end_time=t_s_end)
        s_add.save()

    if quick_appointment:
        # 生成 appointment & invitess
        appointment = Appointment()
        appointment.original_start = t_s_start
        appointment.original_end = t_s_end
        appointment.scheduled_time = t_s_start
        appointment.event_subscription = s_add
        appointment.save()
        appointment.hosts.add(s_add.event.user)
        appointment.invitees.add(s_add.invitee)

        vc = VirtualClass()
        vc.appointment = appointment
        vc.original_start = t_s_start
        vc.original_end = t_s_end
        # vc.scheduled_time = t_s_start
        vc.session_id = VirtualClass.generate_session_id()
        vc.event_subscription = s_add
        vc.save()

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