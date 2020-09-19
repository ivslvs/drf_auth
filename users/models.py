# import pyotp
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')


class User(AbstractUser):
    """Extended User model"""
    email = models.EmailField(max_length=255, unique=True, verbose_name='email address')
    passport_number = models.CharField(max_length=10, unique=True, blank=False, null=False,
                                       validators=[alphanumeric], verbose_name='passport number')

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
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=ACTIVATED, verbose_name="user's status")
    is_active = models.BooleanField(default=True)


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """Balance automatically creates for user"""
    if created:
        Balance.objects.create(client=instance)


class Balance(models.Model):
    """User's balance"""
    client = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, verbose_name='client')
    balance = models.DecimalField(default=0, max_digits=10, decimal_places=10, verbose_name="user's name")
