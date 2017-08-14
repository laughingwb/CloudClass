from django.contrib import admin

# Register your models here.
from .models import Event, EventSubscription, Appointment
# Register your models here.
admin.site.register(Event)
admin.site.register(EventSubscription)
admin.site.register(Appointment)
# admin.site.register(ChangeRequest)