#-----------------------------Написание примитивной ORM-----------------------------


import sqlite3

"""Внутри каждой функции прописываем соединение с БД, курсор, коммит и закрытие соединения с БД"""


def initiate_db():
    """создаёт таблицы Products и Users, если они ещё не созданы при помощи SQL запроса. """
    connection = sqlite3.connect('Products.db')
    cursor = connection.cursor()
    cursor.execute('''
CREATE TABLE IF NOT EXISTS Products(
id INTEGER PRIMARY KEY,
title TEXT NOT NULL,
description TEXT,
price INTEGER NOT NULL
)
''')
    connection = sqlite3.connect('Users.db')
    cursor = connection.cursor()
    cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER NOT NULL,
balance INTEGER NOT NULL
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


def add_user(username, email, age):
    """добавляет в таблицу Users БД запись с переданными данными. Баланс у новых пользователей всегда равен 1000"""
    connection = sqlite3.connect('Users.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)',
                   [f'{username}', f'{email}', f'{age}', 1000])
    connection.commit()
    connection.close()


def is_included(username):
    """Принимает имя пользователя и возвращает True, если такой пользователь есть в таблице Users, в противном случае False. """
    connection = sqlite3.connect('Users.db')
    cursor = connection.cursor()
    cursor.execute('SELECT COUNT(*) FROM Users WHERE username = ?', (username,))
    included = cursor.fetchone()
    connection.close()
    return included[0] > 0

