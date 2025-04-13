from django.db import models
from django.contrib.auth.models import AbstractUser
from config.util_models.models import TimeStampdModels
from django.utils import timezone
from datetime import timedelta


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=32, unique=True)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number']

class EmailVerificationCode(TimeStampdModels):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)


    def is_expiered(self):
        return timezone.now > self.created_at + timedelta(minutes=10)