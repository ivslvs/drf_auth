from django.core.mail import send_mail
from django.conf import settings
from rest_framework import serializers
from accounts.models import User


class ActivationSerializer(serializers.HyperlinkedModelSerializer):
    client = serializers.HyperlinkedIdentityField(view_name='client_activation')

    class Meta:
        model = User
        fields = ['client']


class DeactivationSerializer(serializers.HyperlinkedModelSerializer):
    client = serializers.HyperlinkedIdentityField(view_name='client_deactivation')

    class Meta:
        model = User
        fields = ['client']


class ClientUnregisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'status', 'is_active']

    # нужна ли валидация
    def update(self, instance, validated_data):
        if instance.status == 'RA':
            User.objects.filter(id=instance.id).update(is_active=True)

        elif instance.status == 'RD':
            User.objects.filter(id=instance.id).update(is_active=False)

        # send_mail(subject='Registration confirmation', message="Your registration have completed successfully.",
        #           recipient_list=[instance.email], from_email=settings.EMAIL_HOST_USER)

        return User.objects.get(id=instance.id)

