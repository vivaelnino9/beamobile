from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

from simple_email_confirmation.models import SimpleEmailConfirmationUserMixin

from .choices import *

class Organization(models.Model):
    name = models.CharField(verbose_name='Name',max_length=50)
    class Meta:
        db_table = 'organizations'

    def __str__(self):
        return self.name

class Location(models.Model):
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50,choices=STATE_CHOICES)
    zip_code = models.PositiveIntegerField()
    class Meta:
        db_table = 'locations'

    def __str__(self):
        return self.address

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
    organization = models.ForeignKey(Organization,null=True,on_delete=models.SET_NULL)
    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.email

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
    is_main_challenge = models.BooleanField(default=False)
    is_bonus_challenge = models.BooleanField(default=False)
    class Meta:
        db_table = 'challenges'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        diff = self.date_end - self.date_start
        self.time_left = diff.days
        if self.is_main_challenge and Challenge.objects.filter(is_main_challenge=True).exists():
            challenge = Challenge.objects.filter(is_main_challenge=True)
            challenge.update(is_main_challenge=False)
        elif self.is_bonus_challenge and Challenge.objects.filter(is_bonus_challenge=True).exists():
            challenge = Challenge.objects.filter(is_bonus_challenge=True)
            challenge.update(is_bonus_challenge=False)
        super(Challenge, self).save(*args, **kwargs)
class Challenge_Status(models.Model):
    user = models.ForeignKey(
        User,
        related_name='user',
        null=True,
        on_delete=models.SET_NULL
    )
    challenge = models.OneToOneField(Challenge)
    status = models.CharField(
        choices=STATUS_CHOICES,
        default=1,
        max_length=50
    )
    location = models.ForeignKey(
        Location,
        related_name='location',
        null=True,
        on_delete=models.SET_NULL
    )
    class Meta:
        db_table = 'challenge_status'

    def __str__(self):
        return self.status
