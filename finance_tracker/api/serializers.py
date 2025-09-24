from rest_framework import serializers
from core.models import Transaction, Category, TelegramProfile

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class TelegramProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "username", "telegram_id")  # добавляем telegram_id