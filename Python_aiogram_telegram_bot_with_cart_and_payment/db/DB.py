import sqlite3


class Database:
    """
    Класс описывает модель БД и основные функции для разработки Корзин на сайтах и чат-ботах
    При создании таблицы пользователей в БД рекомендуется задать изначальный параметр active = 1
    для отслеживания статуса пользователей
    """

    def __init__(self, db_file, users_table: str, catalog_table: str, cart_table: str, order_table: str):
        """
        Подготовка к инициализации класса Database
        :param db_file: Файл с необходимой БД
        :param users_table: Таблица пользователей в БД
        :param catalog_table: Таблица каталога товаров в БД
        :param cart_table: Таблица корзин пользователей в БД
        """
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        self._users_table = users_table
        self._catalog_table = catalog_table
        self._cart_table = cart_table
        self._order_table = order_table

    @property
    def users_table(self):
        return self._users_table

    @property
    def catalog_table(self):
        return self._catalog_table

    @property
    def cart_table(self):
        return self._cart_table

    @property
    def order_table(self):
        return self._order_table

    def sql_start(self):
        """
        Метод для подключения БД и вывода текстового сообщения
        """
        with self.connection:
            #     self.cursor.execute(f'CREATE TABLE IF NOT EXISTS {self.users_table}(user_id INT NOT NULL PRIMARY KEY,'
            #                         f'user_name    TEXT    NOT NULL,'
            #                         f'user_surname TEXT,'
            #                         f'username     TEXT,'
            #                         f'active       INT     DEFAULT 1,'
            #                         f'user_phone   INTEGER)')
            #     self.cursor.execute(f'CREATE TABLE IF NOT EXISTS {self.catalog_table}'
            #                         f'(prod_id INTEGER NOT NULL PRIMARY KEY UNIQUE,'
            #                         f'prod_name        TEXT,'
            #                         f'prod_description TEXT,'
            #                         f'prod_price       INTEGER DEFAULT 100 NOT NULL,'
            #                         f'prod_photo       INTEGER)')
            #     self.cursor.execute(f'CREATE TABLE IF NOT EXISTS {self.cart_table}(user_id  INT     NOT NULL,'
            #                         f'prod_id  INT     NOT NULL,'
            #                         f'quantity INTEGER DEFAULT 1 NOT NULL)')
            #     self.connection.commit()
            if self.connection:
                return 'База подключена'

    def exist_in_users_table(self, select_colum: str, user_id: int) -> bool:
        """
        Метод для проверки наличия пользователя в таблице пользователей
        :param select_colum: Название столбца для проверки
        :param user_id: Уникальный ID пользователя
        :return: Булевое значение
        """
        with self.connection:
            result = self.cursor.execute(
                f"SELECT {select_colum} FROM {self._users_table} WHERE user_id = {user_id}").fetchone()
            return bool(result)

    def add_user(self, user_id: int, user_name: str, user_surname: str, username: str):
        """
        Метод по добавлению нового пользователя в таблицу пользователей
        :param user_id: Уникальный ID пользователя
        :param user_name: Имя пользователя
        :param user_surname: Фамилия пользователя
        :param username: Ник пользователя
        """
        with self.connection:
            return self.cursor.execute(
                f"INSERT INTO {self.users_table} (user_id, user_name, user_surname, username) VALUES (?, ?, ?, ?)",
                (user_id, user_name, user_surname, username))

    def get_users(self) -> list:
        """
        Метод получения всех активных пользователей из таблицы пользователей
        :return: Список уникальных ID пользователей
        """
        with self.connection:
            return self.cursor.execute(f"SELECT user_id, active FROM {self.users_table}").fetchall()

    def get_user_name(self, user_id: int) -> str:
        """
        Метод получения ника пользователя по уникальному ID из таблицы пользователей
        :param user_id: Уникальный ID пользователя
        :return: Список с одним значением
        """
        with self.connection:
            return self.cursor.execute(f"SELECT username FROM {self.users_table} "
                                       f"WHERE user_id = {user_id}").fetchone()

    def set_active(self, user_id: int, active: int):
        """
        Метод для изменения статуса пользователя - активен/не активен в таблице пользователей
        :param user_id: Уникальный ID пользователя
        :param active: Значение статуса пользователя 1 - активен, 0 - не активен
        :return: Обновляет статус пользователя в таблице пользователей
        """
        with self.connection:
            # return self.cursor.execute((f"UPDATE 'people' SET 'active' = {active} WHERE 'user_id'  = {user_id}"))
            return self.cursor.execute(f"UPDATE {self.users_table} SET active = ? "
                                       f"WHERE user_id = ?", (active, user_id))

    def add_contact(self, user_id: int, user_phone: int):
        """
        Метод добавляет в таблицу номер телефона пользователя в таблице пользователей
        :param user_id: Уникальный ID пользователя
        :param user_phone: Номер телефона пользователя
        :return: Обновляет номер пользователя в таблице пользователей
        """
        with self.connection:
            return self.cursor.execute(f"UPDATE {self.users_table} SET user_phone = ?"
                                       f" WHERE user_id = ?", (user_phone, user_id))

    def get_all_items(self) -> list:
        """
        Метод получения всех товаров из таблицы товаров
        :return: Список товаров
        """
        with self.connection:
            return self.cursor.execute(
                f"SELECT prod_id, prod_photo, prod_name, prod_description, prod_price FROM "
                f"{self.catalog_table}").fetchall()

    def get_item_quantity_from_user_cart(self, user_id: int, prod_id: int) -> int:
        """
        Метод для получения количества товара из таблицы корзин пользователей
        :param user_id: Уникальный ID пользователя
        :param prod_id: Уникальный ID товара
        :return: Значение количества товара
        """
        with self.connection:
            return self.cursor.execute(
                f"SELECT quantity FROM {self.cart_table} WHERE user_id = {user_id} "
                f"AND prod_id = {prod_id}").fetchone()

    def add_item_to_cart(self, user_id: int, prod_id: int, quantity: int):
        """
        Метод для добавления товара в корзину пользователя
        :param user_id: Уникальный ID пользователя
        :param prod_id: Уникальный ID товара
        :param quantity: Количество товара
        :return: Добавляет товар в таблицу корзин пользователей
        """
        with self.connection:
            return self.cursor.execute(f"INSERT INTO {self.cart_table} (user_id, prod_id, quantity) VALUES (?, ?, ?)",
                                       (user_id, prod_id, quantity))

    def user_in_cart_exist(self, user_id: int, prod_id: int = 'prod_id'):
        """
        Метод проверяет есть ли пользователь с определенным товаром в таблице корзин пользователей
        :param user_id: Уникальный ID пользователя
        :param prod_id: Уникальный ID товара
        :return: Булевое значение
        """
        with self.connection:
            result = self.cursor.execute(
                f"SELECT user_id FROM {self.cart_table} WHERE user_id = {user_id} AND prod_id = {prod_id}").fetchone()
            return bool(result)

    def change_item_quantity_in_cart(self, user_id: int, prod_id: int, quantity: int):
        """
        Метод для изменения количества товара в корзине пользователя
        :param user_id: Уникальный ID пользователя
        :param prod_id: Уникальный ID товара
        :param quantity: Количество товара
        :return: Обновление количества товара в корзине пользователя
        """
        with self.connection:
            return self.cursor.execute(f"UPDATE {self.cart_table} SET quantity = {quantity} WHERE user_id = {user_id} "
                                       f"AND prod_id = {prod_id}").fetchone()

    def delete_item_from_user_cart(self, user_id: int, prod_id: int):
        """
        Метода для удаления товара из корзины пользователя
        :param user_id: Уникальный ID пользователя
        :param prod_id: Уникальный ID товара
        :return: Удаляет товар из корзины пользователя
        """
        with self.connection:
            return self.cursor.execute(f"DELETE FROM {self.cart_table} WHERE user_id= {user_id} AND "
                                       f"prod_id = {prod_id}").fetchone()

    def get_user_cart(self, user_id: int) -> dict:
        """
        Метод для получения товаров из корзины пользователя с их названием и ценой из таблицы каталога
        :param user_id: Уникальный ID пользователя
        :return: Словарь со значениями товаров корзины пользователя
        """
        with self.connection:
            new_data_from_cart = {}
            data_from_cart = self.cursor.execute(
                f"SELECT prod_id, quantity FROM {self.cart_table} WHERE user_id = {user_id}").fetchall()
            for i in range(len(data_from_cart)):
                prod_name = self.cursor.execute(f"SELECT prod_name FROM {self.catalog_table} WHERE "
                                                f"prod_id={data_from_cart[i][0]}").fetchone()
                prod_name = ''.join(prod_name[0])
                prod_price = self.cursor.execute(f"SELECT prod_price FROM {self.catalog_table} WHERE "
                                                 f"prod_id={data_from_cart[i][0]}").fetchone()
                prod_price = prod_price[0] * data_from_cart[i][1]
                # prod_price = int(''.join(map(str, prod_price[0]))) * data_from_cart[i][1]
                new_data_from_cart[prod_name] = [data_from_cart[i][0], prod_price, data_from_cart[i][1]]
            return new_data_from_cart

    def delete_user_cart(self, user_id: int):
        """
        Метод для полной очистки корзины пользователя
        :param user_id: Уникальный ID пользователя
        :return: Удалеяет все товары из корзины пользователя
        """
        with self.connection:
            return self.cursor.execute(f"DELETE FROM {self.cart_table} WHERE user_id= {user_id}").fetchall()

    def fill_order_table(self, user_id, user_nik, user_name, user_phone,
                         total_amount, products, shipment, user_address,
                         created, is_track_number_send=False, is_order_send=False):
        with self.connection:
            return self.cursor.execute(f"INSERT INTO {self.order_table} (user_id, user_nik, user_name, "
                                       f"user_phone, total_amount,products, shipment, user_address,"
                                       f" created, is_track_number_send, is_order_send) "
                                       f"VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                       (user_id, user_nik, user_name, user_phone, total_amount,
                                        products, shipment, user_address,
                                        created, is_track_number_send, is_order_send))

    def get_user_track_number(self, user_id: int):
        with self.connection:
            track_number_list = self.cursor.execute(
                f'SELECT track_number, is_track_number_send FROM {self.order_table} '
                f'WHERE user_id= {user_id}').fetchall()
            for i in range(len(track_number_list)):
                if track_number_list[i][0] and not track_number_list[i][1]:
                    return track_number_list[i][0]

    def update_track_number_status(self, user_id: int, track_number: int):
        with self.connection:
            return self.cursor.execute(f"UPDATE {self.order_table} SET is_track_number_send = True WHERE"
                                       f" user_id = {user_id} AND track_number = {track_number}").fetchone()
