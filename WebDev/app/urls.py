from django.urls import path

from .views import PrizesListAPIView, UserPrizeCreateAPIView, UserKeyCheckAPIView


urlpatterns = [
    path('prizes/', PrizesListAPIView.as_view(), name='Призы'),
    path('check-user/', UserKeyCheckAPIView.as_view(), name='check_user'),
    path('prize_user/', UserPrizeCreateAPIView.as_view(), name='Выйгрыш'),
]