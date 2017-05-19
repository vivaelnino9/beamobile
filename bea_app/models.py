from django.db import models
from django.contrib.auth.models import AbstractUser
from simple_email_confirmation.models import SimpleEmailConfirmationUserMixin

class User(SimpleEmailConfirmationUserMixin,AbstractUser):
    email = models.EmailField(max_length=255)
    zip_code = models.CharField(
        max_length=5,
        default='',
    )
    points = models.PositiveIntegerField(blank=True,null=True,default=0)
    class Meta:
        db_table = 'users'
