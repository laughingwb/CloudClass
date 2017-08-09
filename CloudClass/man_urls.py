from django.conf.urls import url
from userprofile import views as user_view

urlpatterns = [
    url(r'^$', user_view.man_home, name='man_home'),
]