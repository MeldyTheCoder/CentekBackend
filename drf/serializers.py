from rest_framework import serializers
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


class SpeicalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Speciality
        fields = ('id', 'name')


class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    speciality = SpeicalitySerializer()

    class Meta:
        model = Doctor
        fields = ('id','first_name', 'last_name', 'surname', 'description', 'user', 'speciality')


class ConsultationSerializer(serializers.ModelSerializer):
    from_doctor = DoctorSerializer()
    to_user = UserSerializer()

    class Meta:
        model = Consultation
        fields = ('id','date_created', 'from_doctor', 'to_user')


class ConsultationMessage(serializers.ModelSerializer):
    from_user = UserSerializer()
    consultation = ConsultationSerializer()

    class Meta:
        model = ConsultationMessage
        fields = ('id', 'from_user', 'consultation', 'message', 'attachments')


class ReviewSerializer(serializers.ModelSerializer):
    from_user = UserSerializer()
    to_doctor = DoctorSerializer()

    class Meta:
        model = Review
        fields = ('id', 'from_user', 'to_doctor', 'rate', 'message')


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'avatar')

    def update(self, instance, validated_data):
        image = validated_data.pop('avatar', None)

        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)

        if image is not None:
            instance.image.save(image.name, image.read(), save=False)
            instance.image.save()

        instance.save()

        return instance


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'from_user', 'to_doctor', 'rate', 'message', 'consultation')
