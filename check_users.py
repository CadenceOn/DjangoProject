import sqlite3

# Подключаемся к базе данных Flask API (путь может быть другим)
conn = sqlite3.connect("db.sqlite3.db")
cursor = conn.cursor()

# Проверяем, есть ли таблица пользователей
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user';")
table_exists = cursor.fetchone()

if table_exists:
    # Выводим всех пользователей
    cursor.execute("SELECT * FROM user;")
    users = cursor.fetchall()
    print("Пользователи в базе данных:", users)
else:
    print("Таблица 'user' не найдена. Возможно, база пуста или миграции не выполнены.")

conn.close()
