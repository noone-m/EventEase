from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from .models import OTP, User, PasswordChangeRequested

class TokenSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label=_("Email"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style = {'input_type' : 'password'}, write_only = True,max_length=128)
    class Meta:
        model = User
        fields = ['id','first_name', 'last_name', 'email', 'phone', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data):
        if validated_data['password'] != validated_data['password2']:
            raise serializers.ValidationError({'error' : 'the first password doesn\'t match the second one'})
        
        if User.objects.filter(email = validated_data['email']).exists():
            raise serializers.ValidationError({'error' : 'Email already exists'})
        
        user = User.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            password=validated_data['password']
        )
        return user

class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name', 'last_name', 'email', 'phone', 'password', 'is_active', 'is_service_provider', 'is_superuser', 'last_login', 'date_joined']
        extra_kwargs = {'password': {'write_only': True}}

    
class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = ['id','code','user','service','expire_date', 'is_verified']
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True},
            'service': {'read_only': True},
            'expire_date': {'read_only': True},
            'is_verified': {'read_only': True},
        }

class ChangePasswordRequestedSerialzer(serializers.Serializer):
    """
    Serializer class for handling change password requests.

    This serializer validates the request by checking if the provided email address
    exists in the User model. It raises a validation error if the email is not found.
    """

    email = serializers.EmailField()
    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email not found")
        return value


class ChangePasswordRequestsSerializer(serializers.ModelSerializer):
    """
    Serializer class to handle list passwords requests
    """
    class Meta:
        model = PasswordChangeRequested
        fields = '__all__'

class UpdatePasswordSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style = {'input_type' : 'password'}, write_only = True,max_length=128)
    _email = serializers.EmailField()
    class Meta:
        model = User
        fields = ['_email', 'password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data
    
    def update(self, user, validated_data):
        user.password = make_password(validated_data['password'])
        user.save()
        return user

