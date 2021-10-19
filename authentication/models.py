from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
	verified = models.BooleanField(default=False)
	certification_text = models.TextField(blank=True, null=True)
	certification_number = models.CharField(max_length=50, blank=True, null=True)
	profile_picture = models.FileField(upload_to='agents/', blank=True)
	stamp = models.FileField(upload_to='agents/stamp/', blank=True)
	is_inspector = models.BooleanField(default=False)

	def __str__(self):
		return self.username

