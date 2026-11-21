from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=11, blank=True, null=True)
    
    USER_TYPES = (
        ('customer', 'مشتری'),
        ('admin', 'مدیر'),
    )
    user_type = models.CharField(
        max_length=20, 
        choices=USER_TYPES, 
        default='customer'
    )

    def str(self):
        return self.username