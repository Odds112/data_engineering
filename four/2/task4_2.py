import sqlite3
import csv

# Подключение к базе данных SQLite
conn = sqlite3.connect('tournament_data.db')
cursor = conn.cursor()

# Создание таблицы для новых данных
cursor.execute('''
    CREATE TABLE IF NOT EXISTS prizes (
        id INTEGER PRIMARY KEY,
        name TEXT,
        place INTEGER,
        prize INTEGER,
        tournament_id INTEGER,
        FOREIGN KEY (tournament_id) REFERENCES tournaments(id)
    )
''')
conn.commit()

# Загрузка данных из CSV файла в базу данных
with open('task_2_var_30_subitem.csv', newline='', encoding='utf-8') as csvfile:
    csv_reader = csv.DictReader(csvfile, delimiter=';')
    for row in csv_reader:
        cursor.execute('''
            INSERT INTO prizes (name, place, prize, tournament_id)
            VALUES (?, ?, ?, (SELECT id FROM tournaments WHERE name = ?))
        ''', (
            row['name'],
            int(row['place']),
            int(row['prise']),
            row['name']
        ))

conn.commit()

# Выполнение запросов, использующих связь между таблицами
# Примеры запросов (замените их на свои):
# 1. Вывести все призы (name, place, prize) для турнира с id=1
query1 = '''
    SELECT p.name, p.place, p.prize
    FROM prizes p
    WHERE p.tournament_id = 1
'''
cursor.execute(query1)
result1 = cursor.fetchall()
print("Query 1:")
for x in result1:
    print(x)

# 2. Вывести средний приз для всех турниров
query2 = '''
    SELECT AVG(p.prize)
    FROM prizes p
'''
cursor.execute(query2)
result2 = cursor.fetchone()[0]
print("\nQuery 2:")
print(f"Average Prize: {result2}")

# 3. Вывести турниры (name, begin), у которых есть призы более 1_000_000
query3 = '''
    SELECT t.name, t.begin
    FROM tournaments t
    WHERE EXISTS (
        SELECT 1
        FROM prizes p
        WHERE p.tournament_id = t.id AND p.prize > 1000000
    )
'''
cursor.execute(query3)
result3 = cursor.fetchall()
print("\nQuery 3:")
print(result3)

# Закрытие соединения с базой данных
conn.close()
