import os
import uuid
from django.db import models
from django.db.models.fields.related import ForeignKey

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('cw', filename)
# Create your models here.

class Programme(models.Model):
    programme_name = models.CharField(max_length = 50)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.programme_name

class Course(models.Model):
    programme = ForeignKey(Programme, on_delete=models.CASCADE)
    course_level = models.IntegerField()
    course_name = models.CharField(max_length=50)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.course_name

class Session(models.Model):
    course = ForeignKey(Course, on_delete=models.CASCADE)
    session_no = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def _get_session_name(self):
        # course_name = Course.objects.get(id=self.course.id).course_name
        # return '%s - lesson %s' % (course_name, self.session_no)
        return 'lesson {0}'.format(self.session_no)

    session_name = property(_get_session_name)

    def __str__(self):
        return self.course.course_name +'-' + self.session_name


class Courseware(models.Model):
    session = ForeignKey(Session, on_delete=models.CASCADE)
    cw_type = models.CharField(max_length=20, choices=(('ppt', 'ppt'), ('image', 'image')), default='image')
    # cw_content = models.FileField(upload_to='cw/%Y/%m')
    cw_content = models.FileField(upload_to=get_file_path)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = (
            ("can_upload_courseware", "Can upload courseware"),
        )

    def __str__(self):
        return self.session.course.course_name + '-' + self.session.session_name
