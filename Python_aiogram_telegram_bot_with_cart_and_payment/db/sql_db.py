import sqlite3 as sq
import psycopg2
# from config import DB_URL
from psycopg2 import Error


def sql_start():
    global base, cur
    base = sq.connect('db/TESTDB.db')
    cur = base.cursor()
    if base:
        print('База подключена')
    base.close()


async def db_table_val(user_id: int, user_name: str, user_surname: str, username: str):
    global base, cur
    base = sq.connect('db/TESTDB.db')
    cur = base.cursor()
    try:
        cur.execute(f"SELECT user_id FROM people WHERE user_id = {user_id}")
        result = cur.fetchone()
        if not result:
            cur.execute('INSERT INTO people(user_id, user_name, user_surname, username) VALUES (?, ?, ?, ?)',
                        (user_id, user_name, user_surname, username))
            base.commit()
            base.close()
        base.close()
    except (Exception, sq.DatabaseError) as error:
        print("Ошибка в транзакции.", error)
        try:
            cur.close()
            cur = base.cursor()
        except:
            base.close()
            base = sq.connect('db/TESTDB.db')
            cur = base.cursor()

# async def user_exist(self, user_id):
# 	with self.connection:
# 		result = self.cursor.execute(f"SELECT user_id FROM people WHERE user_id = {user_id}").fetchmany(1)
# 		return bool(len(result))
#
#
# async def add_user(self, user_id: int, user_name: str, user_surname: str, username: str):
# 	with self.connection:
# 		return self.cursor.execute(
# 			"INSERT INTO 'people' ('user_id', 'user_name', 'user_surname', 'username') VALUES (?, ?, ?, ?)",
# 			(user_id, user_name, user_surname, username))
#
#
# async def set_active(self, user_id, active):
# 	with self.connection:
# 		return self.cursor.execute((f"UPDATE 'people' SET 'active' = {active} WHERE 'user_id'  = {user_id}"))
#
#
# async def get_users(self):
# 	with self.connection:
# 		return self.cursor.execute(f"SELECT user_id, active FROM people").fetchall()
