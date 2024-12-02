from rest_framework import serializers

from .models import Prizes, UserPrize, UserKey


class UserPrizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPrize
        fields = ['user', 'prize']

# Сериализатор для модели UserKey
class UserKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserKey
        fields = ['id', 'full_name', 'secret_key', 'created_at']

# Сериализатор для модели Prizes
class PrizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prizes
        fields = ['id', 'text', 'img']

# Сериализатор для связи между UserKey и Prizes
class UserPrizeSerializer(serializers.ModelSerializer):
    user = UserKeySerializer(read_only=True)
    prize = PrizeSerializer(read_only=True)

    class Meta:
        model = UserPrize
        fields = ['user', 'prize']


