from django.conf.urls import url

from . import views as scheduler_view

urlpatterns = [
    url(r'^entry/',scheduler_view.entry, name='entry'),
    url(r'^entry_tutor/',scheduler_view.entry_tutor, name='scheduler_entry_tutor'),
    url(r'^calendar/',scheduler_view.calendar, name='calendar'),
    url(r'^scheduler_publish/',scheduler_view.scheduler_publish, name='scheduler_publish'),
    url(r'^delete_event/',scheduler_view.delete_event, name='scheduler_delete_event'),
    url(r'^event/', scheduler_view.event, name='scheduler_event'),
    url(r'^subscribe/',scheduler_view.subscribe, name='scheduler_subscribe'),
]