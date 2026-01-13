from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import *

@receiver(post_save, sender=CustomUser)
def permissions_update(sender, instance, created, **kwargs):
    
    pass