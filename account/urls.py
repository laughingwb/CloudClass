from django.conf.urls import url
from . import views as account_views

urlpatterns = [
    url(r'^signup/',account_views.signup, name='signup'),
    url(r'^loginhtml/',account_views.loginhtml, name='loginhtml'),
    url(r'^signupAccount/',account_views.signupAccount, name='signupAccount'),
    url(r'^loginAccount/',account_views.loginAccount, name='loginAccount'),
    url(r'^logoutAccount/',account_views.logoutAccount, name='logoutAccount'),
]