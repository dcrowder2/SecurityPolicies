from django.db import models


# Create your models here.
class Programs(models.Model):
	name = models.CharField(max_length=32)
	groups = (
		("A", "Admin"),
		("SE", "Software Engineer"),
		("U", "User")
	)
	permission_level = models.CharField(max_length=2, choices=groups)

	def __str__(self):
		return self.name
