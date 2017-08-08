from django.db import models
from django.utils.translation import ugettext_lazy as _
# Create your models here.


class UserInfo(models.Model):
    username = models.CharField(max_length = 50)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    email = models.CharField(max_length = 50)
    GENDER_CHOICES = (
        ('Male', _('Male')),
        ('Female', _('Female')),
        ('N/A', _('N/A')),
    )
    gender = models.CharField(max_length=30, choices=GENDER_CHOICES, null=True, blank=True)  # Male：男； Female：女
    birthdate = models.DateField(blank=True, null=True)
    phone_num = models.CharField(max_length=30, null=True, blank=True)
    def __str__(self):
        return self.username
