from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from exam.models import CustomUser, Question


class CustomUserSerializer(UserCreateSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username', 'password')


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
