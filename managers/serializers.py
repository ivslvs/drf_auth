from django.core.mail import send_mail
from django.conf import settings
from rest_framework import serializers
from users.models import User


class ActivationDeactivationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email']


class ClientStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'status', 'is_active']

    def update(self, instance, validated_data):

        if instance.status == 'RA':
            instance.is_active = True
            instance.status = 'A'

        elif instance.status == 'RD':
            instance.is_active = False
            instance.status = 'D'

        instance.save()

        # send_mail(subject='Registration confirmation', message="Your registration have completed successfully.",
        #           recipient_list=[instance.email], from_email=settings.EMAIL_HOST_USER)

        return instance
