import sqlite3
from datetime import date
from datetime import datetime


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
    """Возвращает все задания из базы данных начиная с текущей даты."""
    now_date = date.today().strftime("%Y-%m-%d")  # Текущая дата в формате ГГГГ-ММ-ДД

    conn = create_connection()
    cursor = conn.cursor()
    
    # Преобразуем дату в формате ГГГГ-ММ-ДД для корректного сравнения
    cursor.execute('SELECT date, subject, homework FROM homework')
    rows = cursor.fetchall()
    conn.close()

    # Фильтруем и сортируем внутри Python, если даты хранятся в ДД.ММ.ГГГГ
    valid_rows = []
    for hw_date, subject, task in rows:
        try:
            # Преобразуем в формат datetime для сравнения
            hw_date_obj = datetime.strptime(hw_date, "%d.%m.%Y").date()
            if hw_date_obj >= date.today():  # Включаем текущий день
                valid_rows.append((hw_date, subject, task))
        except ValueError:
            continue  # Пропускаем некорректные даты

    # Сортируем по дате (по объектам date)
    valid_rows.sort(key=lambda hw: datetime.strptime(hw[0], "%d.%m.%Y").date())

    return valid_rows




def delete_homework(date, subject):
    """Удаляет домашнее задание из базы данных по дате и названию предмета."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM homework WHERE date = ? AND subject = ?
    ''', (date, subject))
    conn.commit()
    conn.close()

def delete_old_homework():
    conn = sqlite3.connect("homework.db")  # Подключаемся к БД
    cursor = conn.cursor()

    # Получаем текущую дату в формате ДД.ММ.ГГГГ
    today = datetime.today().strftime("%d.%m.%Y")

    # Удаляем все записи, у которых дата раньше сегодняшней
    cursor.execute("DELETE FROM homework WHERE date < ?", (today,))

    conn.commit()
    conn.close()