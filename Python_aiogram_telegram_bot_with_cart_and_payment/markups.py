from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from aiogram.types import ReplyKeyboardRemove, KeyboardButton
from aiogram.utils.callback_data import CallbackData

hide_kb = ReplyKeyboardRemove()

kb = CallbackData('cb', 'id', 'action')

kb_users = CallbackData('kb', 'id')


def generate_start_kb():
    catalog = InlineKeyboardButton("Каталог", callback_data='catalog')
    cart = InlineKeyboardButton("Корзина", callback_data='cart')
    manager = InlineKeyboardButton("Связь с менеджером", url='https://t.me/python_inter')
    start_kb = InlineKeyboardMarkup(row_width=1)
    start_kb.add(catalog, cart, manager)
    return start_kb


def generate_catalog_kb():
    order = InlineKeyboardButton("Заказать", callback_data='order')
    back = InlineKeyboardButton("Назад", callback_data='back_to_start')
    cart = InlineKeyboardButton("Корзина", callback_data='cart')
    manager = InlineKeyboardButton("Связь с менеджером", url='https://t.me/python_inter')
    catalog_kb = InlineKeyboardMarkup(row_width=1)
    catalog_kb.add(cart, order, manager, back)
    return catalog_kb


def generate_order_kb(user_id):
    order = InlineKeyboardButton("Заказать", callback_data='order')
    update = InlineKeyboardButton("Обновить Стоимость Корзины", callback_data='cart')
    delete_all = InlineKeyboardButton("Очистить Корзину", callback_data=kb.new(id=user_id, action='delete_all'))
    manager = InlineKeyboardButton("Связь с менеджером", url='https://t.me/python_inter')
    back = InlineKeyboardButton("Назад", callback_data='back_to_start')
    order_kb = InlineKeyboardMarkup(row_width=1)
    order_kb.add(order, update, delete_all, manager, back)
    return order_kb


def generate_contact_kb():
    contact = KeyboardButton("Поделится номером телефона", request_contact=True)
    contact_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    contact_kb.add(contact)
    return contact_kb


def generate_add_kb(prod_id, action):
    add = InlineKeyboardButton("Добавить в корзину", callback_data=kb.new(id=prod_id, action=action))
    add_kb = InlineKeyboardMarkup(row_width=1)
    add_kb.add(add)
    return add_kb


def generate_delete_kb(prod_id, action):
    delete = InlineKeyboardButton("Удалить товар из корзины", callback_data=kb.new(id=prod_id, action=action))
    delete_kb = InlineKeyboardMarkup(row_width=1)
    delete_kb.add(delete)
    return delete_kb


def generate_add_and_delete_kb(prod_id, add_action, delete_action, count):
    add = InlineKeyboardButton("+", callback_data=kb.new(id=prod_id, action=add_action))
    value = InlineKeyboardButton(f"{count}", callback_data='value')
    delete = InlineKeyboardButton("-", callback_data=kb.new(id=prod_id, action=delete_action))
    add_and_delete_kb = InlineKeyboardMarkup(row_width=3)
    add_and_delete_kb.add(delete, value, add)
    return add_and_delete_kb


def generate_cat_kb():
    catalog = InlineKeyboardButton("Каталог", callback_data='catalog')
    manager = InlineKeyboardButton("Связь с менеджером", url='https://t.me/python_inter')
    cat_kb = InlineKeyboardMarkup(row_width=1)
    cat_kb.add(catalog, manager)
    return cat_kb


def generate_buy_kb():
    buy = InlineKeyboardButton("Оплатить заказ", callback_data='buy')
    manager = InlineKeyboardButton("Связь с менеджером", url='https://t.me/python_inter')
    back = InlineKeyboardButton("Назад", callback_data='back_to_cart')
    buy_kb = InlineKeyboardMarkup(row_width=1)
    buy_kb.add(buy, manager, back)
    return buy_kb


def generate_provider_kb():
    yookassa = InlineKeyboardButton("Ю Касса", callback_data='yookassa')
    sber = InlineKeyboardButton("Сбербанк", callback_data='sber')
    manager = InlineKeyboardButton("Связь с менеджером", url='https://t.me/python_inter')
    provider_kb = InlineKeyboardMarkup(row_width=2)
    provider_kb.add(yookassa, sber, manager)
    return provider_kb
