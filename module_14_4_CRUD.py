# -----------------------написать простейшие CRUD функции для взаимодействия с базой данных.-----------------------

import sqlite3

"""Внутри каждой функции прописываем соединение с БД, курсор, коммит и закрытие соединения с БД"""


def initiate_db():
    connection = sqlite3.connect('Products.db')
    cursor = connection.cursor()
    """создаёт таблицу Products, если она ещё не создана при помощи SQL запроса. Эта таблица содержит следующие поля:
id - целое число, первичный ключ
title(название продукта) - текст (не пустой)
description(описание) - текст
price(цена) - целое число (не пустой)"""
    cursor.execute('''
CREATE TABLE IF NOT EXISTS Products(
id INTEGER PRIMARY KEY,
title TEXT NOT NULL,
description TEXT,
price INTEGER NOT NULL
)
''')
    connection.commit()
    connection.close()


def len_db():  # определяет количество строк базы данных
    connection = sqlite3.connect('Products.db')  # подключение к базе данных
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Products')
    users = cursor.fetchall()
    connection.commit()
    connection.close()
    return len(users)


def get_all_products():
    """возвращает все записи из таблицы Products, полученные при помощи SQL запроса."""
    connection = sqlite3.connect('Products.db')  # подключение к базе данных
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Products')
    users = cursor.fetchall()
    total_list = {}
    for user in users:
        list_ = []
        for i in user:
            list_.append(i)
        total_list[user[0]] = list_
    connection.commit()
    connection.close()
    return total_list  # возвращает словарь с записями из таблицы, где ключом будет id
