from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Logon(models.Model):
	logon_attempts = 0
	user = models.ForeignKey(User, on_delete=models.CASCADE)
