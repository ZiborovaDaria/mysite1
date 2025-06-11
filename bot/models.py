from django.db import models

from goods.models import Products
from main.models import Store
from users.models import User


class Feedback(models.Model):
    FEEDBACK_TYPES = [
        ('shop', 'О магазине'),
        ('product', 'О товаре'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    telegram_user_id = models.BigIntegerField(verbose_name="ID пользователя Telegram")
    username = models.CharField(max_length=100, blank=True, verbose_name="Имя пользователя")
    feedback_type = models.CharField(
        max_length=10, 
        choices=FEEDBACK_TYPES,
        verbose_name="Тип отзыва"
    )
    product = models.ForeignKey(
        Products,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Товар"
    )
    store = models.ForeignKey(
        Store,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Магазин"
    )
    rating = models.PositiveSmallIntegerField(verbose_name="Оценка")
    text = models.TextField(verbose_name="Текст отзыва")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_handled = models.BooleanField(default=False, verbose_name="Обработан")
    forwarded_to_operator = models.BooleanField(default=False, verbose_name="Передано оператору")

    def __str__(self):
        return f"Отзыв от {self.username} ({self.rating}/5)"
