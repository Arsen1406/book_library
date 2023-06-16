# Generated by Django 3.2.19 on 2023-06-16 08:41

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('book', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Rentals',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('create_date', models.DateTimeField(default=datetime.datetime(2023, 6, 16, 8, 41, 54, 755539, tzinfo=utc), verbose_name='Время аренды')),
                ('return_date', models.DateTimeField(default=datetime.datetime(2023, 6, 30, 8, 41, 54, 755554, tzinfo=utc), verbose_name='Дата возврата')),
                ('books', models.ManyToManyField(to='book.Book', verbose_name='Аренда книг')),
                ('reader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reader', to=settings.AUTH_USER_MODEL, verbose_name='Читатель')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
    ]