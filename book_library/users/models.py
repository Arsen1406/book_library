from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
        'password',
    ]
    id = models.AutoField(primary_key=True)
    email = models.EmailField(
        'email address',
        max_length=254,
        unique=True,
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Читатель'
        verbose_name_plural = 'Читатели'

    def __str__(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        return self.username
