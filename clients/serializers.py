from rest_framework import serializers
from accounts.models import Balance, User


class BalanceSerializers(serializers.ModelSerializer):
    class Meta:
        model = Balance
        fields = '__all__'


class ClientDeletionSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']

    def update(self, instance, validated_data):
        User.objects.filter(id=instance.id).update(status='RD')
        return User.objects.get(id=instance.id)
