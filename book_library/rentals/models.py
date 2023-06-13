import datetime
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.timezone import now
from book.models import Book

User = get_user_model()


class Rentals(models.Model):
    id = models.AutoField(primary_key=True)
    books = models.ManyToManyField(Book, verbose_name='Аренда книг')
    reader = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reader',
        verbose_name='Читатель'
    )
    create_date = models.DateTimeField(
        default=now(),
        verbose_name='Время аренды'
    )
    return_date = models.DateTimeField(
        default=now() + datetime.timedelta(days=14),
        verbose_name='Дата возврата'
    )

    def __str__(self):
        return f'Заказ - {self.pk}, до {self.return_date}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
