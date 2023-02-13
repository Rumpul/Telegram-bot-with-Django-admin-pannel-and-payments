from django.contrib import admin

from .forms import PeopleForm, CatalogForm
from .models import People, Catalog, Cart, Order


# Register your models here.
@admin.register(People)
class PeopleAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'user_name', 'user_surname',
                    'username', 'user_phone', 'active')
    form = PeopleForm


@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    list_display = ('prod_id', 'prod_name', 'prod_description',
                    'prod_price', 'prod_photo')
    form = CatalogForm


@admin.register(Cart)
class CatalogAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'prod_id', 'quantity')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'user_nik', 'user_name',
                    'user_phone', 'total_amount', 'products',
                    'shipment', 'user_address', 'track_number', 'is_track_number_send', 'is_order_send', 'created')
    list_filter = ('created', 'is_track_number_send', 'is_order_send')
    search_fields = ('user_id', 'user_nik', 'user_name',
                     'user_phone', 'total_amount', 'products',
                     'shipment', 'user_address', 'track_number', 'created', 'is_track_number_send', 'is_order_send')
