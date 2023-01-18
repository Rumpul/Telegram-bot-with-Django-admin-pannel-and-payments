import sqlite3


class Database:
    """
    Класс описывает модель БД и основные функции для разработки Корзин на сайтах и чат-ботах
    При создании таблицы пользователей в БД рекомендуется задать изначальный параметр active = 1
    для отслеживания статуса пользователей
    """

    def __init__(self, db_file, users_table: str, catalog_table: str, cart_table: str):
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

    @property
    def users_table(self):
        return self._users_table

    @property
    def catalog_table(self):
        return self._catalog_table

    @property
    def cart_table(self):
        return self._cart_table

    def sql_start(self):
        """
        Метод для подключения БД и вывода текстового сообщения
        """
        with self.connection:
            print('База подключена')

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
                f"INSERT INTO {self._users_table} (user_id, user_name, user_surname, username) VALUES (?, ?, ?, ?)",
                (user_id, user_name, user_surname, username))


    def get_users(self) -> list:
        """
        Метод получения всех активных пользователей из таблицы пользователей
        :return: Список уникальных ID пользователей
        """
        with self.connection:
            return self.cursor.execute(f"SELECT user_id, active FROM {self._users_table}").fetchall()

    def get_user_name(self, user_id: int) -> str:
        """
        Метод получения ника пользователя по уникальному ID из таблицы пользователей
        :param user_id: Уникальный ID пользователя
        :return: Список с одним значением
        """
        with self.connection:
            return self.cursor.execute(f"SELECT username FROM {self._users_table} "
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
            return self.cursor.execute(f"UPDATE {self._users_table} SET active = ? "
                                       f"WHERE user_id = ?", (active, user_id))

    def add_contact(self, user_id: int, user_phone: int):
        """
        Метод добавляет в таблицу номер телефона пользователя в таблице пользователей
        :param user_id: Уникальный ID пользователя
        :param user_phone: Номер телефона пользователя
        :return: Обновляет номер пользователя в таблице пользователей
        """
        with self.connection:
            return self.cursor.execute(f"UPDATE {self._users_table} SET user_phone = ?"
                                       f" WHERE user_id = ?", (user_phone, user_id))

    def get_all_items(self) -> list:
        """
        Метод получения всех товаров из таблицы товаров
        :return: Список товаров
        """
        with self.connection:
            return self.cursor.execute(
                f"SELECT prod_id, prod_photo, prod_name, prod_description, prod_price FROM {self._catalog_table}").fetchall()

    def get_item_quantity_from_user_cart(self, user_id: int, prod_id: int) -> int:
        """
        Метод для получения количества товара из таблицы корзин пользователей
        :param user_id: Уникальный ID пользователя
        :param prod_id: Уникальный ID товара
        :return: Значение количества товара
        """
        with self.connection:
            return self.cursor.execute(
                f"SELECT quantity FROM {self._cart_table} WHERE user_id = {user_id} "
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
            return self.cursor.execute(f"INSERT INTO {self._cart_table} (user_id, prod_id, quantity) VALUES (?, ?, ?)",
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
                f"SELECT user_id FROM {self._cart_table} WHERE user_id = {user_id} AND prod_id = {prod_id}").fetchone()
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
            return self.cursor.execute(f"UPDATE {self._cart_table} SET quantity = {quantity} WHERE user_id = {user_id} "
                                       f"AND prod_id = {prod_id}").fetchone()

    def delete_item_from_user_cart(self, user_id: int, prod_id: int):
        """
        Метода для удаления товара из корзины пользователя
        :param user_id: Уникальный ID пользователя
        :param prod_id: Уникальный ID товара
        :return: Удаляет товар из корзины пользователя
        """
        with self.connection:
            return self.cursor.execute(f"DELETE FROM {self._cart_table} WHERE user_id= {user_id} AND "
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
                f"SELECT prod_id, quantity FROM {self._cart_table} WHERE user_id = {user_id}").fetchall()
            for i in range(len(data_from_cart)):
                prod_name = self.cursor.execute(f"SELECT prod_name FROM {self._catalog_table} WHERE "
                                                f"prod_id={data_from_cart[i][0]}").fetchone()
                prod_name = ''.join(prod_name[0])
                prod_price = self.cursor.execute(f"SELECT prod_price FROM {self._catalog_table} WHERE "
                                                 f"prod_id={data_from_cart[i][0]}").fetchone()
                prod_price = prod_price[0] * data_from_cart[i][1]
                #prod_price = int(''.join(map(str, prod_price[0]))) * data_from_cart[i][1]
                new_data_from_cart[prod_name] = [data_from_cart[i][0], prod_price, data_from_cart[i][1]]
            return new_data_from_cart

    def delete_user_cart(self, user_id: int):
        """
        Метод для полной очистки корзины пользователя
        :param user_id: Уникальный ID пользователя
        :return: Удалеяет все товары из корзины пользователя
        """
        with self.connection:
            return self.cursor.execute(f"DELETE FROM {self._cart_table} WHERE user_id= {user_id}").fetchall()
