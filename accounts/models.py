# accounts/models.py

from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
    name = models.CharField(max_length=200, unique=True)
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name