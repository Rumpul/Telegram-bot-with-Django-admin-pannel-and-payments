# Generated by Django 4.1.5 on 2023-02-10 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bot', '0016_delete_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.BigIntegerField(verbose_name='ID пользователя')),
                ('user_nik', models.TextField(verbose_name='Ник пользователя')),
                ('user_name', models.TextField(verbose_name='Имя пользователя')),
                ('user_phone', models.IntegerField(blank=True, null=True, verbose_name='Телефон пользователя')),
                ('total_amount', models.IntegerField(verbose_name='Сумма')),
                ('products', models.TextField(verbose_name='Товары в заказе')),
                ('shipment', models.TextField(verbose_name='Способ отправки')),
                ('user_address', models.TextField(verbose_name='Адрес отправки')),
                ('track_number', models.IntegerField(blank=True, default=None, null=True, verbose_name='Трек номер пользователя')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('processed', models.BooleanField(default=False, verbose_name='Заказ обработан')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
                'db_table': 'orders',
            },
        ),
    ]