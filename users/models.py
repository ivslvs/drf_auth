import pyotp
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')


class User(AbstractUser):
    """Override User model"""

    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    passport_number = models.CharField(max_length=10, unique=True, blank=False, null=False, validators=[alphanumeric])

    ACTIVATION = 'RA'
    DEACTIVATION = 'RD'
    ACTIVATED = 'A'
    DEACTIVATED = 'D'
    STATUS_CHOICES = [
        (ACTIVATION, 'require activation'),
        (DEACTIVATION, 'require deactivation'),
        (ACTIVATED, 'activated'),
        (DEACTIVATED, 'deactivated'),
    ]
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=ACTIVATED)
    is_active = models.BooleanField(default=True)


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Balance.objects.create(client=instance)


class Balance(models.Model):
    """Balance"""
    client = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    balance = models.DecimalField(default=0, max_digits=10, decimal_places=10)
