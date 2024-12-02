import secrets
from django.db import models
import uuid


class Prizes(models.Model):
    """Призы"""
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    text = models.CharField(max_length=200, verbose_name='Название')
    quantity = models.PositiveIntegerField(
        default=0,
        verbose_name="Количество",
        help_text="Количество доступных экземпляров этого приза"
    )
    probability = models.FloatField(
        default=0.1,  # По умолчанию 10%
        verbose_name="Шанс выпадения",
        help_text="Вероятность выпадения приза (например, 0.1 = 10%)"
    )
    img = models.ImageField("изображение", upload_to="img/",
                            help_text='Поддерживаются изображения формата JPG, PNG.', blank=True, null=True)

    class Meta:
        verbose_name = 'Приз'
        verbose_name_plural = "Призы"

    def __str__(self):
        return f"{self.text} (Доступно: {self.quantity}, Шанс: {self.probability * 100:.1f}%)"

    def reduce_quantity(self):
        """Уменьшает количество призов на 1, если доступно"""
        if self.quantity > 0:
            self.quantity -= 1
            self.save()
        else:
            raise ValueError("Недостаточно призов в наличии")



class UserKey(models.Model):
    """Модель для хранения ФИО пользователя и уникального ключа"""
    full_name = models.CharField(max_length=255, verbose_name="ФИО пользователя")
    secret_key = models.CharField(
        max_length=16,
        unique=True,
        editable=False,
        verbose_name="Уникальный ключ"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def save(self, *args, **kwargs):
        if not self.secret_key:
            self.secret_key = secrets.token_urlsafe(12)[:16]
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Ключ пользователя"
        verbose_name_plural = "Ключи пользователей"

    def __str__(self):
            return self.full_name


class UserPrize(models.Model):
    """Модель для связи пользователя и приза"""
    user = models.ForeignKey(UserKey, on_delete=models.CASCADE, verbose_name="Пользователь")
    prize = models.ForeignKey(Prizes, on_delete=models.CASCADE, verbose_name="Приз")
    redeemed_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата получения")

    class Meta:
        verbose_name = "Связь пользователя и приза"
        verbose_name_plural = "Связи пользователей и призов"
        unique_together = ("user", "prize")

    def __str__(self):
        return f"{self.user.full_name} - {self.prize.text}"

    def save(self, *args, **kwargs):
        if self.pk is None:  # Только при создании новой записи
            if self.prize.quantity > 0:
                self.prize.reduce_quantity()  # Уменьшаем количество доступных призов
            else:
                raise ValueError("Приз недоступен для выдачи")
        super().save(*args, **kwargs)
