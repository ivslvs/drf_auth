from rest_framework import serializers
from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'passport_number', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def save(self):
        account = User(
            email=self.validated_data['email'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            passport_number=self.validated_data['passport_number']
        )
        password = self.validated_data['password']

        if account.is_superuser is False:
            account.is_active = True

        account.set_password(password)
        account.save()
