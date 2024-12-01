from rest_framework import generics, status
from rest_framework.response import Response
from .models import UserKey, Prizes, UserPrize
from .serializers import UserPrizeSerializer, PrizeSerializer, UserKeySerializer
from django.shortcuts import get_object_or_404

class PrizesListAPIView(generics.ListAPIView):
    serializer_class = PrizeSerializer

    def get_queryset(self):
        # Фильтруем призы, у которых количество больше 0
        return Prizes.objects.filter(quantity__gt=0).order_by('id')

class UserKeyCheckAPIView(generics.GenericAPIView):
    serializer_class = UserKeySerializer

    def get(self, request, *args, **kwargs):
        secret_key = request.query_params.get('secret_key')

        if not secret_key:
            return Response({"detail": "Параметр 'secret_key' обязателен."}, status=status.HTTP_400_BAD_REQUEST)

        # Получаем пользователя по secret_key
        try:
            user = UserKey.objects.get(secret_key=secret_key)
        except UserKey.DoesNotExist:
            return Response({"detail": "Пользователь с таким ключом не найден."}, status=status.HTTP_404_NOT_FOUND)

        # Проверяем, участвовал ли пользователь ранее
        has_participated = UserPrize.objects.filter(user=user).exists()
        if has_participated:
            return Response({"detail": "Пользователь уже участвовал."}, status=status.HTTP_403_FORBIDDEN)

        # Сериализуем данные о пользователе
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserPrizeCreateAPIView(generics.CreateAPIView):
    serializer_class = UserPrizeSerializer

    def create(self, request, *args, **kwargs):
        secret_key = request.data.get('secret_key')
        prize_id = request.data.get('prize_id')

        if not secret_key or not prize_id:
            return Response({"detail": "Параметры 'secret_key' и 'prize_id' обязательны."}, status=status.HTTP_400_BAD_REQUEST)

        # Получаем пользователя по secret_key
        user = get_object_or_404(UserKey, secret_key=secret_key)

        # Получаем приз по prize_id
        prize = get_object_or_404(Prizes, id=prize_id)

        # Проверяем, не получал ли уже пользователь этот приз
        if UserPrize.objects.filter(user=user, prize=prize).exists():
            return Response({"detail": "Приз уже был получен этим пользователем."}, status=status.HTTP_400_BAD_REQUEST)

        # Создаем запись о получении приза
        user_prize = UserPrize.objects.create(user=user, prize=prize)

        # Сериализуем данные
        serializer = self.get_serializer(user_prize)

        return Response(serializer.data, status=status.HTTP_201_CREATED)