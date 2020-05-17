from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.validators import RegexValidator
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import Group

alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')


class ClientManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, passport_number, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not first_name:
            raise ValueError('Users must have a first_name')
        if not last_name:
            raise ValueError('Users must have a last_name')
        if not passport_number:
            raise ValueError('Users must have a password_number')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            passport_number=passport_number
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, passport_number, password):
        user = self.create_user(email, first_name, last_name, passport_number, password=password)
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Client(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address (case-sensitive)', max_length=255, unique=True)
    first_name = models.CharField(max_length=15, blank=False, null=False)
    last_name = models.CharField(max_length=15, blank=False, null=False)
    passport_number = models.CharField(max_length=10, unique=True, blank=False, null=False, validators=[alphanumeric])

    # status для манагеров по которому они активируют\деактивирую пользователя
    # после выхода из системы (log out), status = requires deactivation
    status = models.CharField(default='requires activation', max_length=25, auto_created=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'passport_number']

    objects = ClientManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin or self.is_superuser

    def has_module_perms(self, app_label):
        return True


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Balance(models.Model):
    """Balance"""

    email = models.OneToOneField(Client, primary_key=True, on_delete=models.CASCADE)
    balance = models.DecimalField(default=0, max_digits=10, decimal_places=10)


class CustomGroup(models.Model):
    """Override Group model"""

    group = models.OneToOneField(Group, unique=True, on_delete=models.DO_NOTHING)
    users = models.OneToOneField(Client, on_delete=models.DO_NOTHING)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        print('method save()')
        return

    def __str__(self):
        return
