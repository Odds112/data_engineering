import sqlite3
import json
import msgpack

# Подключение к базе данных SQLite (если ее нет, она будет создана)
conn = sqlite3.connect('tournament_data.db')
cursor = conn.cursor()

# Создание таблицы в базе данных
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tournaments (
        id INTEGER PRIMARY KEY,
        name TEXT,
        city TEXT,
        begin TEXT,
        system TEXT,
        tours_count INTEGER,
        min_rating INTEGER,
        time_on_game INTEGER
    )
''')
conn.commit()

# Добавление данных из msgpack файла в базу данных
with open('task_1_var_30_item.msgpack', 'rb') as f:
    data = msgpack.unpackb(f.read(), raw=False)

    for tournament in data:
        cursor.execute('''
            INSERT INTO tournaments (id, name, city, begin, system, tours_count, min_rating, time_on_game)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            tournament['id'],
            tournament['name'],
            tournament['city'],
            tournament['begin'],
            tournament['system'],
            tournament['tours_count'],
            tournament['min_rating'],
            tournament['time_on_game']
        ))

conn.commit()

# Задайте произвольные значения для переменных
VAR = 5

# Вывод первых (VAR+10) отсортированных по произвольному числовому полю строк в файл формата JSON
query1 = f'SELECT * FROM tournaments ORDER BY time_on_game LIMIT {VAR + 10}'
cursor.execute(query1)
result1 = cursor.fetchall()

with open('result1.json', 'w', encoding='utf-8') as json_file:
    json.dump(result1, json_file, ensure_ascii=False, indent=2)

# Вывод (сумма, мин, макс, среднее) по произвольному числовому полю
numerical_field = 'min_rating'
query2 = f'SELECT SUM({numerical_field}), MIN({numerical_field}), MAX({numerical_field}), AVG({numerical_field}) FROM tournaments'
cursor.execute(query2)
result2 = cursor.fetchone()
print(f"Statistics for {numerical_field}: Sum={result2[0]}, Min={result2[1]}, Max={result2[2]}, Avg={result2[3]}")

# Вывод частоты встречаемости для категориального поля
categorical_field = 'system'
query3 = f'SELECT {categorical_field}, COUNT(*) FROM tournaments GROUP BY {categorical_field}'
cursor.execute(query3)
result3 = cursor.fetchall()
categorical_frequency = {row[0]: row[1] for row in result3}
print(f"Frequency of {categorical_field}: {categorical_frequency}")

# Вывод первых (VAR+10) отфильтрованных по произвольному предикату отсортированных по произвольному числовому полю строк в файл формате JSON
predicate_field = 'tours_count'
predicate_value = 5
query4 = f'SELECT * FROM tournaments WHERE {predicate_field} > {predicate_value} ORDER BY {numerical_field} LIMIT {VAR + 10}'
cursor.execute(query4)
result4 = cursor.fetchall()

with open('result4.json', 'w', encoding='utf-8') as json_file:
    json.dump(result4, json_file, ensure_ascii=False, indent=2)

# Закрытие соединения с базой данных
conn.close()
