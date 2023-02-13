from django.db import models


# Create your models here.

class People(models.Model):
    user_id = models.BigIntegerField(primary_key=True,
                                     verbose_name='ID пользователя')
    user_name = models.TextField(verbose_name='Имя пользователя')
    user_surname = models.TextField(blank=True, null=True,
                                    verbose_name='Фамилия пользователя')
    username = models.TextField(blank=True, null=True,
                                verbose_name='Никнейм пользователя')
    active = models.IntegerField(blank=True, null=True,
                                 verbose_name='Состояние активности пользователя')
    user_phone = models.IntegerField(blank=True, null=True,
                                     verbose_name='Телефон пользователя')

    class Meta:
        managed = True
        db_table = 'people'
        verbose_name = 'Пользователь бота'
        verbose_name_plural = 'Пользователи бота'


class Catalog(models.Model):
    prod_id = models.IntegerField(primary_key=True,
                                  verbose_name='ID продукта')
    prod_name = models.TextField(blank=True, null=True,
                                 verbose_name='Название продукта')
    prod_description = models.TextField(blank=True, null=True,
                                        verbose_name='Описание продукта')
    prod_price = models.IntegerField(verbose_name='Цена продукта')
    prod_photo = models.IntegerField(blank=True, null=True,
                                     verbose_name='ID фото продукта')

    class Meta:
        managed = True
        db_table = 'catalog'
        verbose_name = 'Товар'
        verbose_name_plural = 'Таблица товаров'


class Cart(models.Model):
    user_id = models.IntegerField(verbose_name='ID пользователя')
    prod_id = models.IntegerField(verbose_name='ID продукта')
    quantity = models.IntegerField(verbose_name='Количество продукта')

    class Meta:
        db_table = 'cart'
        verbose_name = 'Корзина пользователя'
        verbose_name_plural = 'Таблица корзин пользователей'


class Order(models.Model):
    user_id = models.BigIntegerField(verbose_name='ID пользователя')
    user_nik = models.TextField(verbose_name='Ник пользователя')
    user_name = models.TextField(verbose_name='Имя пользователя')
    user_phone = models.IntegerField(blank=True, null=True,
                                     verbose_name='Телефон пользователя')
    total_amount = models.FloatField(verbose_name='Сумма')
    products = models.TextField(verbose_name='Товары в заказе')
    shipment = models.TextField(verbose_name='Способ отправки')
    user_address = models.TextField(verbose_name='Адрес отправки')
    track_number = models.IntegerField(blank=True, null=True,
                                       verbose_name='Трек номер пользователя')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_track_number_send = models.BooleanField(default=False, verbose_name='Трек номер отправлен')
    is_order_send = models.BooleanField(default=False, verbose_name='Заказ отправлен')

    class Meta:
        db_table = 'orders'
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

