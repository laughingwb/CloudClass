import os, uuid
from django.db import models
from course.models import Course
from django.contrib.auth.models import User
from django.db.models.fields.related import ForeignKey
# Create your models here.

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('avatar', filename)


class Tutor(models.Model):
    user = models.OneToOneField(User)
    course = ForeignKey(Course, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=get_file_path, blank=True)
    introduction = models.TextField(max_length=300, null=True, blank=True)
    score = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.user.username
