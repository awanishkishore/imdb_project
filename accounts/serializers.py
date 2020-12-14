from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, get_user_model
from rest_framework import exceptions
from django.utils.translation import gettext_lazy as _

from accounts.models import User


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('uuid', 'first_name', 'last_name', 'email', 'password')
        extra_kwargs = {
            'uuid': {
                'read_only': True,
            },
            'password': {
                'write_only': True,
                'required': True,
            },
            'first_name': {
                'required': True,
                'write_only': True,
            },
            'last_name': {
                'write_only': True,
            },
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['token'] = Token.objects.get_or_create(user=instance)[0].key
        return representation


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, write_only=True)
    password = serializers.CharField(max_length=128, required=True, write_only=True)

    def validate(self, attrs):
        credentials = {
            get_user_model().USERNAME_FIELD: attrs.get('email'),
            'password': attrs.get('password')
        }
        self.user = authenticate(request=self.context.get('request'), **credentials)

        if self.user is None:
            raise exceptions.AuthenticationFailed(_('Invalid username or password.'))

        if not self.user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))
        return attrs

    @property
    def token(self):
        return {'token': Token.objects.get_or_create(user=self.user)[0].key}