from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields.related import ForeignKey
from functools import cmp_to_key
from django.db.models import Q
from datetime import datetime, timedelta
from django.utils.translation import ugettext as _


class EventManager(models.Manager):
    def get_occurrence_list(tutor, start, end):
        occurrences = []

        events = Event.objects.filter(user=tutor, start__lt=end, end_recurring_period__gte=start)

        for event in events:
            # logger.debug('event item: {0}'.format(event))
            occurrences_of_e = event.get_occurrence_list(start, end)
            occurrences.extend(occurrences_of_e)

        # filter cancelled or changed appointments
        appointments = Appointment.objects.filter(hosts=tutor).filter(
            Q(Q(original_start__gte=start) & Q(original_start__lt=end)) | Q(
                Q(scheduled_time__gte=start) & Q(scheduled_time__lt=end)))
        for a in appointments:
            for o in occurrences:
                # mark time slot available, if the original appointment is cancelled
                if a.original_start == o.start and a.status == Appointment.CANCELLED:
                    o.subscription_start = None
                    o.subscription_end = None
                    o.subscription_invitee = None
                    o.subscription_id = None
                # mark time slot available, if the original appointment is rescheduled
                if a.original_start == o.start and a.scheduled_time != o.start and a.status == Appointment.CONFIRMED:
                    o.subscription_start = None
                    o.subscription_end = None
                    o.subscription_invitee = None
                    o.subscription_id = None
                # mark time slot as taken, if the rescheduled time falls into it
                if a.original_start != o.start and a.scheduled_time == o.start and a.status == Appointment.CONFIRMED:
                    if not o.subscription_id:
                        o.subscription_id = a.event_subscription.id
                        o.subscription_start = a.event_subscription.start_time
                        o.subscription_end = a.event_subscription.end_time
                        o.subscription_invitee = a.event_subscription.invitee.id

        return occurrences

    def get_subscribed_occurrence_list(student, start, end):
        occurrences = []

        event_subscriptions = EventSubscription.objects.filter(invitee=student, start_time__lt=end,
                                                               end_time__gte=start).order_by("start_time")

        for es in event_subscriptions:
            try:
                event = Event.objects.get(pk=es.event.id)
                occurrences_of_e = event.get_occurrence_list(start, end, es)
                for o in occurrences_of_e:
                    if o.start >= es.start_time and o.start < es.end_time:
                        occurrences.append(o)
            except Event.DoesNotExist:
                print('event does not exist')
                # logger.error('event does not exist')

        skey = cmp_to_key(lambda x, y: y.start.timestamp() - x.start.timestamp())
        occurrences.sort(key=skey)

        return occurrences

    def get_unconfirmed_occurrence_list(student, start, end):

        occurrences = EventManager.get_subscribed_occurrence_list(student, start, end)

        for o in occurrences:
            app = Appointment.objects.filter(invitees=student, event_subscription__id=o.subscription_id,
                                             original_start=o.start).first()

            if app:
                occurrences.remove(o)
                print('occurrence is removed: {}'.format(o))
                # logger.debug('occurrence is removed: {}'.format(o))

        return occurrences

# Create your models here.

class Event(models.Model):
    user = ForeignKey(User, on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField(help_text="The end time must be later than the start time.")
    end_recurring_period = models.DateTimeField(null=True, blank=True,help_text="This date is ignored for one time only events.")
    maximum_invitee = models.IntegerField(default=1)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    default_event_duration = 60

    def __str__(self):
        return '{0} ({1} - {2})'.format(self.user.username, self.start, self.end_recurring_period)

class EventSubscription(models.Model):
    event = ForeignKey(Event, on_delete=models.CASCADE)
    invitee = ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{0} ({1} - {2}) : {3}'.format(self.invitee.username, self.start_time, self.end_time, self.event)

class Appointment(models.Model):
    CONFIRMED = 0
    CANCELLED = 1
    STATUS_CHOICES = (
    # 状态 0：确认 1：取消
        (CONFIRMED, 'CONFIRMED'),
        (CANCELLED, 'CANCELLED'),
    )
    original_start = models.DateTimeField()
    original_end = models.DateTimeField()
    schedule_time = models.DateTimeField()
    hosts = models.ManyToManyField(User, related_name='hosts')
    invitees = models.ManyToManyField(User, related_name='invitees')
    status = models.IntegerField(choices=STATUS_CHOICES)
    event_subscription = models.ForeignKey(EventSubscription, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    def __str__(self):
        return '{0}: {1} - {2}'.format(self.scheduled_time, ','.join([h.username for h in self.hosts.all()]),','.join([i.username for i in self.invitees.all()]))

