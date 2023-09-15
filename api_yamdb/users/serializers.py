from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email')


class AuthSerializer(serializers.Serializer):
    username = serializers.SlugField(max_length=150)
    confirmation_code = serializers.CharField(max_length=256)
