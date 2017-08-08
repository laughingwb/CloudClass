from django.conf.urls import url
from . import views as account_views

urlpatterns = [
    url(r'^signup/',account_views.signup, name='signup'),
    url(r'^login/',account_views.login, name='login'),
    url(r'^signupAccount/',account_views.signupAccount, name='signupAccount'),
    url(r'^loginAccount/',account_views.loginAccount, name='loginAccount'),
]