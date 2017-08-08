from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView, RedirectView
from course import views as course_views
from account import views as account_views
from scheduler import views as scheduler_views
from userprofile import views as userprofile_views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='landing_index'),
    url(r'^account/', include('account.urls')),
    url(r'^admin/', include(admin.site.urls)),
]+ static(settings.STATIC_URL) + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
