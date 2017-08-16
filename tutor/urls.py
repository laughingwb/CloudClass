from django.conf.urls import url

from . import views as tutor_view

urlpatterns = [
    url(r'^tutor_list/',tutor_view.tutor_list, name='tutor_list'),
]