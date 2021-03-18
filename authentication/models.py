from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # pass
    # add additional fields in here
    roll_no = models.CharField(unique=True, max_length=9)
    verification_status = models.IntegerField()
    institute_email_id = models.CharField(unique=True, max_length=50)

    def __str__(self):
        return self.username