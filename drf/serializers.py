from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from med.models import *
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(UserCreateSerializer):
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'surname',
            'email',
            'role',
            'avatar',
            'password',
            'first_name',
            'last_name',
            'date_joined',
            'last_login'
        )

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
        )
        user.save()
        return user


# class CustomUserSerializer(UserSerializer):
#     class Meta:
#         model = User
#         fields = '__all__'


class SpeicalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Speciality
        fields = ('id', 'name')


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'avatar')

    def update(self, instance, validated_data):
        image = validated_data.pop('avatar', None)

        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)

        if image is not None:
            instance.image.save(image.name, image.read(), save=False)
            instance.image.save()

        instance.save()

        return instance


class PassportSerializer(serializers.ModelSerializer):
    patient = UserSerializer()

    class Meta:
        model = Passport
        fields = '__all__'


class HospitalizationSerializer(serializers.ModelSerializer):
    patient = UserSerializer()
    passport = PassportSerializer()

    class Meta:
        model = Hospitalization
        fields = '__all__'


class TokenCreateSerializer(TokenObtainPairSerializer):
    pass