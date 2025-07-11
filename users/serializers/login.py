from django.contrib.auth import authenticate
from rest_framework import serializers
from users.models import CustomUser
from django.core.validators import RegexValidator

phone_regex = RegexValidator(
    regex=r'^\+998\d{9}$',
    message='Phone number must be the following: +998 xx xxx xx xx'
)


class UserLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(validators=[phone_regex], max_length=13)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        phone_number = data.get('phone_number')
        password = data.get('password')

        user = authenticate(phone_number=phone_number, password=password)
        if not user:
            raise serializers.ValidationError('Invalid credentials')

        data['user'] = user
        return data
