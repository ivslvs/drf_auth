from django.core.mail import send_mail
from django.conf import settings
from rest_framework import serializers
from accounts.models import User


class ActivationDeactivationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'email']


class UserStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'email', 'status', 'is_active']

    # нужна ли валидация
    def update(self, instance, validated_data):
        if instance.status == 'RA':
            User.objects.filter(pk=instance.pk).update(is_active=True)

        elif instance.status == 'RD':
            User.objects.filter(pk=instance.pk).update(is_active=False)

        send_mail(subject='Registration confirmation', message="Your registration have completed successfully.",
                  recipient_list=[instance.email], from_email=settings.EMAIL_HOST_USER)

        return User.objects.get(pk=instance.pk)

