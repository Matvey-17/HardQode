from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


class CustomUser(AbstractUser):
    """Кастомная модель пользователя - студента."""

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=250,
        unique=True
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name',
        'password'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-id',)

    def __str__(self):
        return self.username


class Balance(models.Model):
    """Модель баланса пользователя."""

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=1000,
        verbose_name='Баланс'
    )

    def save(self, *args, **kwargs):
        if self.balance < 0:
            raise ValidationError(message='Баланс не может быть отрицательным.')
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Баланс'
        verbose_name_plural = 'Балансы'
        ordering = ('-id',)

    def __str__(self):
        return f'Пользователь: {self.user.username} | Баланс: {self.balance}'



