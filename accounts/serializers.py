from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import Client
from rest_framework.authtoken.models import Token


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Client
        fields = ['email', 'first_name', 'last_name', 'passport_number', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def save(self):
        account = Client(
            email=self.validated_data['email'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            passport_number=self.validated_data['passport_number']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        account.set_password(password)
        account.save()
        return account


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError('An email address is required to log in.')

        if password is None:
            raise serializers.ValidationError('A password is required to log in.')

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError('A user with this email and password was not found or deactivated.')

        # if not Client.objects.get(email=email).is_active:
        #     raise serializers.ValidationError('This user has been deactivated.')

        token = Token.objects.get(user=user).key
        return token
