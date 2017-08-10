from django.conf.urls import url

from . import views as scheduler_views

urlpatterns = [
    url(r'^entry/',scheduler_views.entry, name='entry'),
    url(r'^entry_tutor/',scheduler_views.entry_tutor, name='scheduler_entry_tutor'),
    url(r'^calendar/',scheduler_views.calendar, name='calendar'),
]