from unittest.mock import AsyncMock

import pytest

# from Bot import start
# import markups as mar
from db.DB import Database

db = Database('DB_for_tests.db', users_table="people", catalog_table="catalog", cart_table="cart")
user_id = 124129511


def test_db_start():
    expected = 'База подключена'
    assert print(db.sql_start()) is print(expected)


def test_exist_in_users_table():
    assert db.exist_in_users_table("user_id", user_id) is False

# @pytest.mark.asyncio
# async def test_start():
#     message = AsyncMock()
#     await start(message)
#     message.answer.assert_called_with("Вы вернулись в главное меню", reply_markup=mar.generate_start_kb())


# @pytest.mark.asyncio
# async def test_back_to_start():
#     callback = AsyncMock()
#     await back_to_start(callback)
#     callback.message.answer.assert_called_with("Вы вернулись в главное меню", reply_markup=mar.generate_start_kb())
