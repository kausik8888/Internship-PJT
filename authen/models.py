from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=100, blank=False)
    age = models.PositiveIntegerField(null=True, blank=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    email = models.EmailField(unique=True)
    activation_key = models.CharField(max_length=150,blank=True,null=True)
def __str__(self):
        return self.username    