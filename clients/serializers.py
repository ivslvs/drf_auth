from rest_framework import serializers
from accounts.models import Balance, User


class BalanceSerializers(serializers.ModelSerializer):
    class Meta:
        model = Balance
        fields = '__all__'


class ClientDeletionSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'email']

    def update(self, instance, validated_data):
        User.objects.filter(pk=instance.pk).update(status='RD')
        return User.objects.get(pk=instance.pk)
