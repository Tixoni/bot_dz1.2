import sqlite3
from datetime import date


def create_connection():
    """Создает соединение с базой данных SQLite."""
    conn = sqlite3.connect('homework.db')
    return conn

def create_table():
    """Создает таблицу в базе данных."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS homework (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            subject TEXT NOT NULL,
            homework TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_homework(date, subject, homework):
    """Добавляет задание в базу данных."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO homework (date, subject, homework)
        VALUES (?, ?, ?)
    ''', (date, subject, homework))
    conn.commit()
    conn.close()

def get_all_homework():
    now_date = ".".join(str(date.today()).split("-")[1:])
    """Возвращает все задания из базы данных."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT date, subject, homework FROM homework WHERE date >= ? ORDER BY date', (now_date,)) #WHERE date >= ? , (now_date,) проверка по дате.
    rows = cursor.fetchall()
    conn.close()
    return rows