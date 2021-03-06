from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Logon(models.Model):
	logon_attempts = models.IntegerField(default=0)
	user_lockout = models.BooleanField(default=False)
	hard_lockout = models.BooleanField(default=False)
	attempt_time = models.IntegerField(default=0)
	lockouts = models.IntegerField(default=0)
	lockout_time = models.IntegerField(default=0)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
