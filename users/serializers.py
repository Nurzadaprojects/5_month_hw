from rest_framework import serializers
from django.contrib.auth.models import User


class UserCreateSerializers(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate_username(self, username):
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise ValidationError("This username is taken.")



class UserLoginSerializers(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()