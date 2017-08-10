import os, uuid
from django.db import models
from django.utils.translation import ugettext_lazy as _
from course.models import Course
from django.contrib.auth.models import User
from django.db.models.fields.related import ForeignKey
# Create your models here.

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('avatar', filename)

class UserInfo(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(upload_to=get_file_path, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    GENDER_CHOICES = (
        ('Male', _('Male')),
        ('Female', _('Female')),
        ('N/A', _('N/A')),
    )
    gender = models.CharField(max_length=30, choices=GENDER_CHOICES, null=True, blank=True)  # Male：男； Female：女
    birthdate = models.DateField(blank=True, null=True)
    phone_num = models.CharField(max_length=30, null=True, blank=True)
    def __str__(self):
        return self.user.username


