from django.core import validators
from django.utils.timezone import now
from django.db import models


class Author(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    birth_day = models.DateField(
        blank=True,
        null=True,
        verbose_name='Дата рождения'
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Genre(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, verbose_name='Название жанра')
    description = models.CharField(
        max_length=2000,
        blank=True,
        verbose_name='Описание жанра'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, verbose_name='Название книги')
    description = models.CharField(
        max_length=2000,
        blank=True,
        verbose_name='Описание книги'
    )
    author = models.ManyToManyField(Author, verbose_name='Автор')
    genre = models.ManyToManyField(Genre, verbose_name='Жанр')
    remains = models.IntegerField(
        default=0,
        validators=[
            validators.MaxValueValidator(100),
            validators.MinValueValidator(0)
        ],
        verbose_name='Остаток'
    )
    views = models.IntegerField(default=0, verbose_name='Популярность')
    date_create = models.DateField(default=now())

    def __str__(self):
        return (
            f'{self.title}: прочитали {self.views} раз с {self.date_create}'
        )

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
