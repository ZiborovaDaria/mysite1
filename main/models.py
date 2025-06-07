from django.db import models
from django.utils import timezone

class Promotion(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='promotions/', verbose_name='Изображение')
    link = models.CharField(max_length=255, blank=True, null=True, verbose_name='Ссылка')
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title

class Store(models.Model):
    CITY_CHOICES = [
        ('MSK', 'Москва'),
        ('SPB', 'Санкт-Петербург'),
        ('EKB', 'Екатеринбург'),
        ('KZN', 'Казань'),
        ('NNV', 'Нижний Новгород'),
    ]
    
    city = models.CharField(max_length=3, choices=CITY_CHOICES, verbose_name='Город')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Email')
    opening_hours = models.CharField(max_length=100, verbose_name='Часы работы')
    is_main = models.BooleanField(default=False, verbose_name='Главный магазин')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name='Широта')
    longitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name='Долгота')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'
        ordering = ['-is_main', 'city']
    
    def __str__(self):
        return f"{self.get_city_display()}, {self.address}"
    
    def get_map_url(self):
        return f"https://yandex.ru/maps/?text={self.latitude},{self.longitude}"


class Contact(models.Model):
    CONTACT_TYPE_CHOICES = [
        ('PHONE', 'Телефон'),
        ('EMAIL', 'Email'),
        ('ADDRESS', 'Адрес'),
        ('SOCIAL', 'Соцсеть'),
    ]
    
    contact_type = models.CharField(max_length=10, choices=CONTACT_TYPE_CHOICES, verbose_name='Тип контакта')
    value = models.CharField(max_length=255, verbose_name='Значение')
    description = models.CharField(max_length=100, blank=True, verbose_name='Описание')
    is_main = models.BooleanField(default=False, verbose_name='Основной контакт')
    icon = models.CharField(max_length=50, blank=True, verbose_name='Иконка')
    order = models.PositiveSmallIntegerField(default=0, verbose_name='Порядок отображения')

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
        ordering = ['order']
    
    def __str__(self):
        return f"{self.get_contact_type_display()}: {self.value}"