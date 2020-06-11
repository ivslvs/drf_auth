from rest_framework import serializers
from .models import User
from django.core.mail import send_mail
from django.conf import settings


class RegistrationSerializer(serializers.ModelSerializer):
    is_active = serializers.HiddenField(default=False)
    status = serializers.HiddenField(default=User.ACTIVATION)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'passport_number', 'password', 'is_active', 'status']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

        # send_mail(subject='Registration confirmation', message="Please, confirm new client's registration.",
        #           recipient_list=[settings.EMAIL_HOST_USER], from_email='new_client@email.com')