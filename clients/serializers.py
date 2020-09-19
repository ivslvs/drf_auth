from rest_framework import serializers
from users.models import Balance, User


class BalanceSerializers(serializers.ModelSerializer):
    """Client's balance"""
    class Meta:
        model = Balance
        fields = '__all__'


class ClientUnregisterSerializer(serializers.ModelSerializer):
    """Changing user status"""
    status = serializers.HiddenField(default=User.DEACTIVATION)

    class Meta:
        model = User
        fields = ['id', 'email', 'status']
