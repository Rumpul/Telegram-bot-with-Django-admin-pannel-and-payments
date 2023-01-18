from aiogram import types
from aiogram.types import LabeledPrice, ShippingOption


SDEK_SHIPPING_OPTION = ShippingOption(
    id='sdek',
    title='Сдэк'
).add(types.LabeledPrice('Сдэк', 100000))

RUSSIAN_POST_SHIPPING_OPTION = ShippingOption(
    id='ru_post', title='Почтой России')
RUSSIAN_POST_SHIPPING_OPTION.add(
    LabeledPrice(
        'Почта России', 100000)
)

PICKUP_SHIPPING_OPTION = ShippingOption(id='pickup', title='Самовывоз')
PICKUP_SHIPPING_OPTION.add(LabeledPrice('Самовывоз в Москве', 50000))
