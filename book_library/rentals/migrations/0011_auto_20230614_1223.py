# Generated by Django 3.2.19 on 2023-06-14 12:23

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0010_auto_20230614_1055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rentals',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 14, 12, 23, 43, 313198, tzinfo=utc), verbose_name='Время аренды'),
        ),
        migrations.AlterField(
            model_name='rentals',
            name='return_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 28, 12, 23, 43, 313212, tzinfo=utc), verbose_name='Дата возврата'),
        ),
    ]
