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

        return User.objects.get(pk=instance.pk)

