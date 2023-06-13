# Generated by Django 3.2.19 on 2023-06-13 16:00

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0007_auto_20230613_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rentals',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 13, 16, 0, 15, 812350, tzinfo=utc), verbose_name='Время аренды'),
        ),
        migrations.AlterField(
            model_name='rentals',
            name='return_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 27, 16, 0, 15, 812366, tzinfo=utc), verbose_name='Дата возврата'),
        ),
    ]