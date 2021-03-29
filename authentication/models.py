from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

class CustomUser(AbstractUser):
    # pass
    # add additional fields in here
    roll_no = models.CharField(unique=True,max_length=9 ,blank= True)
    verification_status = models.BooleanField(default=False)
    institute_email_id = models.CharField(unique=True, max_length=50, blank= True,validators=[RegexValidator(regex='.+@iitkgp.ac.in', message='Institite email must end with @iitkgp.ac.in', code='nomatch')])

    def __str__(self):
        return self.username