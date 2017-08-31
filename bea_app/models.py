from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from itertools import chain
from operator import attrgetter

from simple_email_confirmation.models import SimpleEmailConfirmationUserMixin

from .choices import *

class Organization(models.Model):
    name = models.CharField(verbose_name='Name',max_length=50)
    class Meta:
        db_table = 'organizations'

    def __str__(self):
        return self.name

    def get_users(self):
        return User.objects.filter(organization=self)

class Location(models.Model):
    address = models.CharField(
        verbose_name='Address',
        max_length=50,
        blank=True,null=True
    )
    city = models.CharField(
        verbose_name='City',
        max_length=50,
        blank=True,null=True
    )
    state = models.CharField(
        verbose_name='State',
        max_length=50,
        choices=STATE_CHOICES,
        blank=True,null=True
    )
    zip_code = models.PositiveIntegerField(
        verbose_name='Zip Code',
        blank=True,null=True
    )
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
    organization = models.ForeignKey(
        Organization,
        verbose_name='Organization',
        null=True,
        on_delete=models.SET_NULL
    )
    redeemed_points = models.PositiveIntegerField(
        verbose_name='Redeemed Points',
        blank=True,null=True,
        default=0
    )
    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.email

    def get_activities(self):
        challenges = Challenge_Status.objects.filter(user=self)
        acts = Act.objects.filter(user=self)
        activities = sorted(
            chain(acts,challenges),
            key=attrgetter('created_on'),
            reverse=True
        )
        return activities
    def get_points(self):
        challenges = Challenge_Status.objects.filter(user=self,status=3)
        challenge_points = 0
        for challenge in challenges:
            challenge_points += challenge.challenge.points
        acts = Act.objects.filter(user=self)
        act_points = len(acts) * 5
        return (challenge_points + act_points)-self.redeemed_points

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
        verbose_name='User',
        related_name='user',
        null=True,
        on_delete=models.CASCADE
    )
    challenge = models.ForeignKey(
        Challenge,
        verbose_name='Challenge',
        related_name='challenge_status',
    )
    status = models.CharField(
        verbose_name='Status',
        choices=STATUS_CHOICES,
        default=1,
        max_length=50
    )
    location = models.ForeignKey(
        Location,
        verbose_name='Location',
        related_name='location',
        blank=True,null=True,
        on_delete=models.SET_NULL
    )
    feeling = models.CharField(
        verbose_name='Feeling',
        max_length=50,
        blank=True,null=True,
    )
    date_completed = models.DateField(verbose_name='Date Completed',blank=True,null=True,)
    created_on = models.DateTimeField(verbose_name='Created On',default=timezone.now)
    class Meta:
        db_table = 'challenge_status'

    def __str__(self):
        return self.status
class Act(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='User',
        related_name='user_act',
        null=True,
        on_delete=models.CASCADE
    )
    name = models.CharField(verbose_name='Name',max_length=50)
    details = models.TextField(verbose_name='Details',max_length=500)
    public = models.BooleanField(verbose_name='Public',default=False)
    created_on = models.DateTimeField(verbose_name='Created On',default=timezone.now)
    class Meta:
        db_table = 'acts'

    def __str__(self):
        return self.name
