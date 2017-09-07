from django.db import models
from opentok import OpenTok
from opentok.opentok import Roles
from django.utils.translation import ugettext as _
from course.models import Session as CourseSession
from scheduler.models import EventSubscription, Appointment
from django.db.models.fields.related import ForeignKey
api_key = '45569802'
api_secret = 'bd18d53d03b50222656a397686c364445900d5f9'
# Create your models here.


class VirtualClass(models.Model):
    class Meta:
        permissions = (
            ("can_monitor_virtualclass", "Can monitor virtualclass"),
        )
    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.CASCADE,
    )
    actual_start = models.DateTimeField(null=True, blank=True)
    actual_end = models.DateTimeField(null=True, blank=True)
    session_id = models.CharField(null=True, blank=True, max_length=100)
    course_session = ForeignKey(CourseSession, on_delete=models.CASCADE, null=True, blank=True)
    is_delivered = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def _get_original_start(self):
        return self.appointment.original_start

    def _get_original_end(self):
        return self.appointment.original_end

    origial_start = property(_get_original_start)
    origial_end = property(_get_original_end)

    def get_scheduled_time(self):
        return self.appointment.scheduled_time

    def get_tutors(self):
        return self.appointment.hosts

    def get_students(self):
        return self.appointment.invitees

    scheduled_time = property(get_scheduled_time)
    tutors = property(get_tutors)
    students = property(get_students)

    ROLE_TUTOR = 'tutor'
    ROLE_STUDENT = 'student'

    def generate_session_id():
        opentok = OpenTok(api_key, api_secret)

        # Create a session that attempts to send streams directly between clients (falling back
        # to use the OpenTok TURN server to relay streams if the clients cannot connect):
        session = opentok.create_session()

        # Store this session ID in the database
        session_id = session.session_id

        # print("generate session:" + session_id)

        return session_id

    def get_token_id(self, username, role=ROLE_STUDENT):
        opentok = OpenTok(api_key, api_secret)
        session_id = self.session_id

        if not session_id:
            return None

        # Generate a Token from just a session_id (fetched from a database)
        connectionMetadata = '{"role":"' + role + '", "username":"' + username + '"}'

        if role == self.ROLE_TUTOR:
            token_id = opentok.generate_token(session_id, Roles.moderator, None, connectionMetadata)
        else:
            token_id = opentok.generate_token(session_id, Roles.publisher, None, connectionMetadata)
        return token_id

    def _get_api_key(self):
        return api_key

    api_key = property(_get_api_key)

    def __str__(self):
        return '{0}: {1} - {2}'.format(self.appointment.scheduled_time,
                                       ','.join([h.username for h in self.appointment.hosts.all()]),
                                       ','.join([i.username for i in self.appointment.invitees.all()]))