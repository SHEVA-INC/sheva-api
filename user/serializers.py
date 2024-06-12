from django.contrib.auth import get_user_model, authenticate, password_validation
from rest_framework import serializers, exceptions

from django.utils.translation import gettext as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "username", "email", "password", "is_staff")
        read_only_fields = ("id", "is_staff")
        extra_kwargs = {"password": {"write_only": True, "min_length": 6}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        """Update a user, set the password correctly and return it"""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


#
#
# class AuthTokenSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField(style={"input_type": "password"})
#
#     def validate(self, data):
#         email = data.get("email")
#         password = data.get("password")
#
#         if email and password:
#             user = authenticate(email=email, password=password)
#
#             if user:
#                 if not user.is_active:
#                     msg = _("User account is disabled.")
#                     raise exceptions.ValidationError(msg)
#             else:
#                 msg = _("Unable to log in with provided credentials.")
#                 raise exceptions.ValidationError(msg)
#         else:
#             msg = _('Must include "email" and "password".')
#             raise exceptions.ValidationError(msg)
#
#         data["user"] = user
#         return data


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['role'] = "admin" if user.is_staff else "user"

        return token


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "username", "email", "first_name", "last_name")
        read_only_fields = ("id",)

