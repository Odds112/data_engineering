import msgpack
import pickle
import sqlite3
import json

# Подключение к базе данных SQLite
conn = sqlite3.connect('combined_data.db')
cursor = conn.cursor()

# Создание таблицы для хранения данных
cursor.execute('''
    CREATE TABLE IF NOT EXISTS songs (
        id INTEGER PRIMARY KEY,
        artist TEXT,
        song TEXT,
        duration_ms INTEGER,
        year INTEGER,
        tempo REAL,
        genre TEXT,
        mode INTEGER,
        speechiness REAL,
        acousticness REAL,
        instrumentalness REAL,
        energy REAL,
        popularity INTEGER
    )
''')
conn.commit()

# Загрузка данных из msgpack файла
with open('task_3_var_30_part_1.msgpack', 'rb') as f:
    data_msgpack = msgpack.unpackb(f.read(), raw=False)

# Загрузка данных из pickle файла
with open('task_3_var_30_part_2.pkl', 'rb') as f:
    data_pickle = pickle.load(f)

# Объединение данных
combined_data = data_msgpack + data_pickle

# Запись данных в базу данных
for song in combined_data:
    cursor.execute('''
        INSERT INTO songs (
            artist, song, duration_ms, year, tempo, genre, mode,
            speechiness, acousticness, instrumentalness, energy, popularity
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        song.get('artist', ''),
        song.get('song', ''),
        int(song.get('duration_ms', 0)),
        int(song.get('year', 0)),
        float(song.get('tempo', 0)),
        song.get('genre', ''),
        int(song.get('mode', 0)),
        float(song.get('speechiness', 0)),
        float(song.get('acousticness', 0)),
        float(song.get('instrumentalness', 0)),
        float(song.get('energy', 0)),
        int(song.get('popularity', 0))
    ))

conn.commit()

# Задайте произвольные значения для переменных
VAR = 5

# Вывод первых (VAR+10) отсортированных по произвольному числовому полю строк в файл формата JSON
query1 = f'SELECT * FROM songs ORDER BY year LIMIT {VAR + 10}'
cursor.execute(query1)
result1 = cursor.fetchall()

with open('result1.json', 'w', encoding='utf-8') as json_file:
    json.dump(result1, json_file, ensure_ascii=False, indent=2)

# Вывод (сумму, мин, макс, среднее) по произвольному числовому полю
numerical_field = 'duration_ms'
query2 = f'SELECT SUM({numerical_field}), MIN({numerical_field}), MAX({numerical_field}), AVG({numerical_field}) FROM songs'
cursor.execute(query2)
result2 = cursor.fetchone()
print(f"Statistics for {numerical_field}: Sum={result2[0]}, Min={result2[1]}, Max={result2[2]}, Avg={result2[3]}")

# Вывод частоты встречаемости для категориального поля
categorical_field = 'genre'
query3 = f'SELECT {categorical_field}, COUNT(*) FROM songs GROUP BY {categorical_field}'
cursor.execute(query3)
result3 = cursor.fetchall()
categorical_frequency = {row[0]: row[1] for row in result3}
print(f"Frequency of {categorical_field}: {categorical_frequency}")

# Вывод первых (VAR+15) отфильтрованных по произвольному предикату отсортированных по произвольному числовому полю строк в файл формата JSON
predicate_field = 'popularity'
predicate_value = 50
query4 = f'SELECT * FROM songs WHERE {predicate_field} > {predicate_value} ORDER BY {numerical_field} LIMIT {VAR + 15}'
cursor.execute(query4)
result4 = cursor.fetchall()

with open('result4.json', 'w', encoding='utf-8') as json_file:
    json.dump(result4, json_file, ensure_ascii=False, indent=2)

# Закрытие соединения с базой данных
conn.close()
