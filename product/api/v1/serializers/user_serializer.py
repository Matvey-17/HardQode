from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework import serializers

from courses.models import Subscription
from users.models import Balance
from api.v1.serializers.course_serializer import CourseSerializer

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    """Сериализатор пользователей."""

    class Meta:
        model = User
        fields = '__all__'


class MiniUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class BalanceSerializer(serializers.ModelSerializer):
    user = MiniUserSerializer()

    class Meta:
        model = Balance
        fields = ['id', 'user', 'balance']


class BalanceAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balance
        fields = ['id', 'user', 'balance']

    def validate(self, data):
        if data['balance'] < 0:
            raise serializers.ValidationError({'error': 'Баланс не может быть отрицательным'})
        return data

    def create(self, validated_data):
        balance = Balance.objects.create(
            user=validated_data['user'],
            balance=validated_data['balance']
        )
        return balance

    def update(self, instance, validated_data):
        instance.balance = validated_data['balance']
        instance.user = validated_data['user']
        instance.save()
        return instance


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор подписки."""

    user = CustomUserSerializer()
    course = CourseSerializer()

    class Meta:
        model = Subscription
        fields = (
            'user',
            'course',
            'is_valid'
        )
