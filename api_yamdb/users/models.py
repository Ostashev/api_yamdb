from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLES = (
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),
    )

    username = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Имя пользователя'
    )
    email = models.EmailField(
        max_length=50,
        unique=True,
        verbose_name='Адрес электронной почты'
    )
    first_name = models.CharField(
        max_length=50,
        verbose_name='Имя',
        null=True)
    last_name = models.CharField(
        max_length=50,
        verbose_name='Фамилия',
        null=True)
    role = models.CharField(
        max_length=50,
        choices=ROLES,
        default='user',
        verbose_name='Роль пользователя'
    )
    bio = models.TextField(
        null=True,
        blank=True,
        verbose_name='Информация о пользователе'
    )
    confirmation_code = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name='Код'
    )


    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
    
    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_user(self):
        return self.role == 'user'


