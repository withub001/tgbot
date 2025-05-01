import sqlite3
from datetime import datetime
connection = sqlite3.connect("kfc.db")
sql = connection.cursor()
# создаем таблицу юзеров
sql.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER, name TEXT,"
            "phone_number TEXT, reg_date DATETIME);")
# создаем таблицу продуктов
sql.execute("CREATE TABLE IF NOT EXISTS products (pr_id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "pr_name TEXT, pr_price REAL, pr_desc TEXT, pr_photo TEXT, pr_quantity INTEGER,"
            "reg_date DATETIME);")
# создаем таблицу корзин пользователей
sql.execute("CREATE TABLE IF NOT EXISTS cart (user_id INTEGER, pr_id INTEGER, pr_name TEXT,"
            "pr_count INTEGER, total_price REAL);")
connection.commit()
# функции для юзеров
# добавление юзера
def add_user(user_id, name, phone_number):
    connection = sqlite3.connect("kfc.db")
    sql = connection.cursor()
    sql.execute(f"INSERT INTO users (user_id, name, phone_number, reg_date) "
                f"VALUES (?, ?, ?, ?);", (user_id, name, phone_number, datetime.now()))
    connection.commit()
# проверка зарегистрирован ли юзер
def check_user(user_id):
    connection = sqlite3.connect("kfc.db")
    sql = connection.cursor()
    check = sql.execute("SELECT * FROM users WHERE user_id=?;", (user_id, )).fetchone()
    # если юзер найден
    if check:
        return True
    # если юзер не найден
    elif not check:
        return False
# получение всех юзеров
def get_all_users():
    connection = sqlite3.connect("kfc.db")
    sql = connection.cursor()
    all_users = sql.execute("SELECT * FROM users;").fetchall()
    return all_users

# функции для работы с продуктами
# добавление продукта
def add_product(pr_name, pr_price, pr_desc, pr_quantity, pr_photo):
    connection = sqlite3.connect("kfc.db")
    sql = connection.cursor()
    sql.execute("INSERT INTO products (pr_name, pr_price, pr_desc, pr_quantity,"
                "pr_photo, reg_date) VALUES (?, ?, ?, ?, ?, ?);",
                (pr_name, pr_price, pr_desc, pr_quantity, pr_photo, datetime.now()))
    connection.commit()
# получение всех продуктов
def get_all_products():
    connection = sqlite3.connect("kfc.db")
    sql = connection.cursor()
    all_product = sql.execute("SELECT * FROM products;").fetchall()
    return all_product
# удаление определенного продукта
def delete_exact_product(pr_id):
    connection = sqlite3.connect("kfc.db")
    sql = connection.cursor()
    sql.execute("DELETE FROM products WHERE pr_id=?;", (pr_id, ))
    connection.commit()
# получение информации об определенном продукте
def get_exact_product(pr_id):
    connection = sqlite3.connect("kfc.db")
    sql = connection.cursor()
    exact_product = sql.execute("SELECT pr_name, pr_price, pr_desc, pr_photo "
                                "FROM products WHERE pr_id=?;", (pr_id, )).fetchone()
    return exact_product
# функция для генерации меню с продуктами
def get_products_id_name():
    connection = sqlite3.connect("kfc.db")
    sql = connection.cursor()
    # вытаскиваем всю информацию о продуктах с которой будет работать
    all_product = sql.execute("SELECT pr_id, pr_name, pr_quantity "
                              "FROM products;").fetchall()
    # фильтруем полученную информацию и оставляем название и айди тех продуктов,
    # количество которых больше 0
    # в каком виде будет выглядеть all_products:
    # [(pr_id, pr_name, pr_quantity), (pr_id, pr_name, pr_quantity), ....]
    actual_products = [[product[0], product[1]] for product in all_product if product[2] > 0]
    # [[pr_id, pr_name], [pr_id, pr_name], ...]
    return actual_products

# дз 1- создать функцию для получения id всех юзеров (get_user_id)
def get_all_id():
    connection = sqlite3.connect("kfc.db")
    sql = connection.cursor()
    all_id = sql.execute("SELECT user_id FROM users;").fetchall()
    return all_id
# 2 - функция для изменения количества продукта (change_pr_quantity)
def change_pr_quantity(pr_id, quantity):
    connection = sqlite3.connect("kfc.db")
    sql = connection.cursor()
    actual_quantity = sql.execute("SELECT pr_quantity FROM products WHERE pr_id=?;", (pr_id, )).fetchone()
    new_quantity = actual_quantity[0] - quantity
    if new_quantity >= 0:
        sql.execute("UPDATE products SET pr_quantity=? WHERE pr_id=?;", (new_quantity, pr_id))
        connection.commit()
        return True
    return False

# 3- функция добавления информации о корзине (add_to_cart)
def add_to_cart(user_id, pr_id, pr_name, pr_price, pr_quantity):
    connection = sqlite3.connect("kfc.db")
    sql = connection.cursor()
    total_price = pr_price * pr_quantity
    sql.execute("INSERT INTO cart (user_id, pr_id, pr_name, pr_count, "
                "total_price) VALUES (?, ? ,? ,?, ?);", (user_id, pr_id,
                                                         pr_name, pr_quantity,
                                                         total_price))
    connection.commit()