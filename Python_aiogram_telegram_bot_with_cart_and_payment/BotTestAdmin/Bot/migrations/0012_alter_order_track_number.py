# Generated by Django 4.1.5 on 2023-02-10 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bot', '0011_order_track_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='track_number',
            field=models.IntegerField(blank=True, default=None, verbose_name='Трек номер пользователя'),
        ),
    ]