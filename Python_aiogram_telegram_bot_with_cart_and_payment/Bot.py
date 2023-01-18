from aiogram import types
from aiogram.utils import executor
from aiogram.types import LabeledPrice
from bot_create import dp, bot, db
import config as conf
import markups as mar
import shipment as ship

print('Бот вышел в онлайн')
db.sql_start()


@dp.message_handler(commands='start')
async def start(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_surname = message.from_user.last_name
    username = message.from_user.username
    await bot.send_message(message.chat.id,
                           text="Привет, {0.first_name}! Я тестовый бот!".format(
                               message.from_user), reply_markup=mar.generate_start_kb())
    if not db.exist_in_users_table("user_id", user_id):
        db.add_user(user_id, user_name, user_surname, username)


@dp.callback_query_handler(text="catalog")
async def catalog(callback: types.CallbackQuery):
    for prod in db.get_all_items():
        await callback.message.answer_photo(prod[1])
        await callback.message.answer(text=f"{prod[2]}\n\n"
                                           f"{prod[3]}\n\n"
                                           f"Стоимость - {prod[4] / 100 :.2f}₽",
                                      reply_markup=mar.generate_add_kb(prod_id=prod[0], action="add"))
    await callback.message.answer(text="По кнопкам ниже Вы можете вернуться в главное меню,оформить заказ и "
                                       "посмотреть корзину",
                                  reply_markup=mar.generate_catalog_kb())
    await callback.answer()


@dp.callback_query_handler(text="back_to_start")
async def back_to_start(callback: types.CallbackQuery):
    await callback.message.answer("Вы вернулись в главное меню", reply_markup=mar.generate_start_kb())
    await callback.answer()


@dp.callback_query_handler(text="cart")
async def cart(callback: types.CallbackQuery):
    user_id = callback.message.chat.id
    total_sum = 0
    if not db.user_in_cart_exist(user_id=user_id):
        await callback.message.answer(text='Ваша корзина пуста(((\n\n'
                                           'Перейдите в каталог и добавьте товар',
                                      reply_markup=mar.generate_cat_kb())
    else:
        for prod_name, prod_data in db.get_user_cart(user_id).items():
            await callback.message.answer(text=f"Название - {prod_name}\n\n"
                                               f"Количество - {prod_data[2]}\n\n"
                                               f"Стоимость - {prod_data[1] / 100 :.2f}₽",
                                          reply_markup=mar.generate_add_and_delete_kb(prod_id=prod_data[0],
                                                                                      add_action="add",
                                                                                      count=prod_data[2],
                                                                                      delete_action="delete")
                                          )

            total_sum += prod_data[1] / 100
        await callback.message.answer(text=f"Итоговая стоимость - {total_sum :.2f}₽\n\n"
                                           f"Для заказа нажмите кнопку ниже:",
                                      reply_markup=mar.generate_order_kb(user_id=user_id))
    await callback.answer()


@dp.callback_query_handler(text="back_to_cart")
async def back_to_start(callback: types.CallbackQuery):
    user_id = callback.message.chat.id
    total_sum = 0
    if not db.user_in_cart_exist(user_id=user_id):
        await callback.message.answer(text='Ваша корзина пуста(((\n\n'
                                           'Перейдите в каталог и добавьте товар',
                                      reply_markup=mar.generate_cat_kb())
    else:
        for prod_name, prod_data in db.get_user_cart(user_id).items():
            await callback.message.answer(text=f"Название - {prod_name}\n\n"
                                               f"Количество - {prod_data[2]}\n\n"
                                               f"Стоимость - {prod_data[1] / 100 :.2f}₽",
                                          reply_markup=mar.generate_add_and_delete_kb(prod_id=prod_data[0],
                                                                                      add_action="add",
                                                                                      count=prod_data[2],
                                                                                      delete_action="delete")
                                          )

            total_sum += prod_data[1] / 100
        await callback.message.answer(text=f"Итоговая стоимость - {total_sum :.2f}₽\n\n"
                                           f"Для заказа нажмите кнопку ниже:",
                                      reply_markup=mar.generate_order_kb(user_id=user_id))
    await callback.answer()


@dp.callback_query_handler(mar.kb.filter(action="add"))
async def add_action(callback: types.CallbackQuery, callback_data: dict):
    prod_id = callback_data.get('id')
    user_id = callback.message.chat.id
    if not db.user_in_cart_exist(user_id=user_id, prod_id=prod_id):
        db.add_item_to_cart(user_id=user_id, prod_id=prod_id, quantity=1)
        await bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
                                            message_id=callback.message.message_id,
                                            reply_markup=mar.generate_add_and_delete_kb(prod_id=prod_id,
                                                                                        add_action="add",
                                                                                        count=1,
                                                                                        delete_action="delete"))
    else:
        # await callback.message.answer(text=db.update_item_quantity_in_cart(user_id=user_id, prod_id=prod_id,
        # quantity=1))
        for row in db.get_item_quantity_from_user_cart(user_id=user_id, prod_id=prod_id):
            quantity = row + 1
            db.change_item_quantity_in_cart(user_id=user_id, prod_id=prod_id, quantity=quantity)
            await bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
                                                message_id=callback.message.message_id,
                                                reply_markup=mar.generate_add_and_delete_kb(prod_id=prod_id,
                                                                                            add_action="add",
                                                                                            count=quantity,
                                                                                            delete_action="delete"))
    await bot.answer_callback_query(callback_query_id=callback.id, text="Добавлено", show_alert=False)


@dp.callback_query_handler(mar.kb.filter(action="delete"))
async def delete_action(callback: types.CallbackQuery, callback_data: dict):
    prod_id = callback_data.get('id')
    user_id = callback.message.chat.id
    if not db.user_in_cart_exist(user_id=user_id, prod_id=prod_id):
        await bot.answer_callback_query(callback_query_id=callback.id, text="Данного товара нет у Вас в корзине",
                                        show_alert=True)
        await bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
                                            message_id=callback.message.message_id,
                                            reply_markup=mar.generate_add_kb(prod_id=prod_id,
                                                                             action="add"))
    else:
        # await callback.message.answer(text=db.update_item_quantity_in_cart(user_id=user_id, prod_id=prod_id,
        # quantity=1))
        for row in db.get_item_quantity_from_user_cart(user_id=user_id, prod_id=prod_id):
            if row > 0:
                quantity = row - 1
                db.change_item_quantity_in_cart(user_id=user_id, prod_id=prod_id, quantity=quantity)
                await bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
                                                    message_id=callback.message.message_id,
                                                    reply_markup=mar.generate_add_and_delete_kb(prod_id=prod_id,
                                                                                                add_action="add",
                                                                                                count=quantity,
                                                                                                delete_action="delete"))
                for quantity in db.get_item_quantity_from_user_cart(user_id=user_id, prod_id=prod_id):
                    if quantity == 0:
                        db.delete_item_from_user_cart(user_id=user_id, prod_id=prod_id)
                        await bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
                                                            message_id=callback.message.message_id,
                                                            reply_markup=mar.generate_add_kb(prod_id=prod_id,
                                                                                             action="add"))
            else:
                try:
                    db.delete_item_from_user_cart(user_id=user_id, prod_id=prod_id)

                except ValueError:
                    print("Ошибка при удалении товара, товар не обнаружен")

                await bot.answer_callback_query(callback_query_id=callback.id,
                                                text="Данного товара нет у Вас в корзине",
                                                show_alert=True)
                await bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
                                                    message_id=callback.message.message_id,
                                                    reply_markup=mar.generate_add_kb(prod_id=prod_id,
                                                                                     action="add"))
    await bot.answer_callback_query(callback_query_id=callback.id, text="Удалено", show_alert=False)


@dp.callback_query_handler(mar.kb.filter(action="delete_all"))
async def delete_all_action(callback: types.CallbackQuery):
    user_id = callback.message.chat.id
    db.delete_user_cart(user_id=user_id)
    await callback.message.answer(text='Ваша корзина очищена\n\n',
                                  reply_markup=mar.generate_cat_kb())
    await callback.answer()


@dp.callback_query_handler(text="order")
async def order(callback: types.CallbackQuery):
    user_id = callback.message.chat.id
    if not db.user_in_cart_exist(user_id=user_id):
        await callback.message.answer(text='Ваша корзина пуста(((\n\n'
                                           'Перейдите в каталог и добавьте товар',
                                      reply_markup=mar.generate_cat_kb())
    else:
        # if db.user_phone_exist(user_id=user_id):
        #     await callback.message.answer(text='Для заказа пожалуйста поделитесь Вашим номером по кнопке ниже:',
        #                                   reply_markup=mar.generate_contact_kb())
        # else:
        #     await callback.message.answer("Пожалуйста оплатите покупки по кнопке ниже:",
        #                                   reply_markup=mar.generate_buy_kb())
        await callback.message.answer("Пожалуйста оплатите покупки по кнопке ниже:",
                                      reply_markup=mar.generate_buy_kb())
    await callback.answer()


@dp.message_handler(content_types=types.ContentType.CONTACT)
async def contacts(message: types.Message):
    await message.answer("Ваш номер успешно получен", reply_markup=mar.hide_kb)
    await message.answer("Пожалуйста оплатите покупки по кнопке ниже:", reply_markup=mar.generate_buy_kb())
    user_id = message.from_user.id
    user_phone = message.contact.phone_number
    if not db.exist_in_users_table("user_phone", user_id):
        db.add_contact(user_id, user_phone)


@dp.callback_query_handler(text="buy")
async def buy(callback: types.CallbackQuery):
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    await callback.message.answer("Пожалуйста выберете способ оплаты", reply_markup=mar.generate_provider_kb())
    await callback.answer()


@dp.callback_query_handler(text="yookassa")
async def yookassa_buy(callback: types.CallbackQuery):
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    user_id = callback.message.chat.id
    prices = [LabeledPrice(label=prod_name, amount=prod_data[1]) for prod_name, prod_data in
              db.get_user_cart(user_id).items()]
    await bot.send_invoice(chat_id=callback.from_user.id,
                           title="Оплата заказа Ю Касса",
                           description="Описание",
                           payload='Заказ',
                           need_name=True,
                           need_phone_number=True,
                           is_flexible=True,
                           provider_token=conf.yootoken,
                           currency="RUB",
                           start_parameter='test_bot',
                           prices=prices)


@dp.callback_query_handler(text="sber")
async def sber_buy(callback: types.CallbackQuery):
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    user_id = callback.message.chat.id
    prices = [LabeledPrice(label=prod_name, amount=prod_data[1]) for prod_name, prod_data in
              db.get_user_cart(user_id).items()]
    await bot.send_invoice(chat_id=callback.from_user.id,
                           title="Оплата заказа Сбербанк",
                           description="Описание",
                           payload='Заказ',
                           need_name=True,
                           need_phone_number=True,
                           is_flexible=True,
                           provider_token=conf.sbertoken,
                           currency="RUB",
                           start_parameter='test_bot',
                           prices=prices)


@dp.shipping_query_handler()
async def process_shipping_query(shipping_query: types.ShippingQuery):
    shipping_options = [
        ship.SDEK_SHIPPING_OPTION,
        ship.RUSSIAN_POST_SHIPPING_OPTION,
    ]
    if shipping_query.shipping_address.country_code == 'RU':
        if shipping_query.shipping_address.city == 'Москва':
            shipping_options.append(ship.PICKUP_SHIPPING_OPTION)

    await bot.answer_shipping_query(
        shipping_query.id,
        ok=True,
        shipping_options=shipping_options
    )


@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
async def process_pay(message: types.Message):
    user_id = message.from_user.id
    if message.successful_payment.invoice_payload == 'Заказ':
        await bot.send_message(message.from_user.id, "Оплата прошла успешно")
        total_amount = message.successful_payment.total_amount // 100
        currency = message.successful_payment.currency
        user_name = message.successful_payment.order_info["name"]
        user_phone = message.successful_payment.order_info["phone_number"]
        user_nik = ''.join(db.get_user_name(user_id))
        shipment = message.successful_payment.shipping_option_id
        if shipment == 'ru_post':
            shipment = "Почта России"
        elif shipment == 'sdek':
            shipment = "Сдэк"
        elif shipment == 'pickup':
            shipment = "Самовывоз"
        user_address = dict(message.successful_payment.order_info["shipping_address"])
        new_address = []
        for value in user_address.values():
            if not value == "" or None:
                new_address.append(value)
        separator = '\n'
        await bot.send_message("", text=f'ЗАКАЗ:\n\n'  # TODO fill the chat or user id who want to get message with information of order 
                                        f'Ник - @{user_nik}\n\n'
                                        f'Имя - {user_name}\n\n'
                                        f'Номер телефона - +{user_phone}\n\n'
                                        f'Итоговая сумма - {total_amount:.2f} {currency}\n\n'
                                        f'Товары :\n'
                                        f'{separator.join([f"{prod_name} : {prod_data[0]} шт" for prod_name, prod_data in db.get_user_cart(user_id).items()])}\n\n'
                                        f'Отправка - {shipment}\n\n'
                                        f'Адрес - {", ".join(new_address)}')
    db.delete_user_cart(user_id)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
