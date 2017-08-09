from django.contrib import admin
from .models import Programme, Course, Session, Courseware
# Register your models here.
admin.site.register(Programme)
admin.site.register(Course)
admin.site.register(Session)
admin.site.register(Courseware)