from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOISE = (
        ('admin', 'admin'),
        ('mentor', 'mentor'),
        ('student', 'student'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOISE, default='student')

    def __str__(self):
        return self.username