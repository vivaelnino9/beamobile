# import datetime
# from datetime import timedelta
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.translation import gettext as _

from address.models import AddressField
from simple_email_confirmation.models import SimpleEmailConfirmationUserMixin

STATUS_CHOICES = (
    (1, _("pending")),
    (2, _("accepted")),
    (3, _("completed")),
)

class User(SimpleEmailConfirmationUserMixin,AbstractUser):
    email = models.EmailField(verbose_name='Email',max_length=255)
    zip_code = models.CharField(
        verbose_name='Zip Code',
        max_length=5,
        default=''
    )
    points = models.PositiveIntegerField(
        verbose_name='Points',
        blank=True,null=True,
        default=0
    )
    class Meta:
        db_table = 'users'

class Challenge(models.Model):
    name = models.CharField(verbose_name='Name',max_length=50)
    details = models.TextField(verbose_name='Details',max_length=500)
    date_start = models.DateField(
        verbose_name='Date Start',
        default=timezone.now,
    )
    date_end = models.DateField(
        verbose_name='Date End',
    )
    time_left = models.PositiveIntegerField(
        verbose_name='Time Left',
        blank=True,null=True,
        default=0
    )
    points = models.PositiveIntegerField(
        verbose_name='Points',
        blank=True,null=True,
        default=0
    )
    location = AddressField(verbose_name='Location',blank=True,null=True,)

    class Meta:
        db_table = 'challenges'

    def save(self, *args, **kwargs):
        diff = self.date_end - self.date_start
        self.time_left = diff.days
        super(Challenge, self).save(*args, **kwargs)
