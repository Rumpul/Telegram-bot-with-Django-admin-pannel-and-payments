# Generated by Django 4.1.5 on 2023-02-10 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bot', '0018_remove_order_processed_order_send'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='track_number',
            field=models.IntegerField(blank=True, null=True, verbose_name='Трек номер пользователя'),
        ),
    ]