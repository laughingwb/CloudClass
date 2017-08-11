from django.conf.urls import url
from . import views as userprofile_views

urlpatterns = [
    url(r'^tutor_profile/',userprofile_views.tutor_profile, name='tutor_profile'),
]