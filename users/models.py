from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    image=models.ImageField(upload_to='user_images',blank=True,null=True,verbose_name='Аватар')
    phone_number = models.CharField(max_length=20, verbose_name="Номер телефона")
    email_verified = models.BooleanField(default=False, verbose_name='Email подтвержден')
    verification_token = models.CharField(max_length=100, blank=True, null=True)
    token_created_at = models.DateTimeField(blank=True, null=True)

    def generate_verification_token(self):
        from django.utils.crypto import get_random_string
        self.verification_token = get_random_string(length=50)
        self.token_created_at = timezone.now()
        self.save()
        return self.verification_token
    
    class Meta:
        db_table='user'
        verbose_name= "Пользователя"
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username