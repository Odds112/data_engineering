import pickle
from pymongo import MongoClient
import numpy as np

# Подключение к MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['task1DB']
collection = db['task1Coll']

# Загрузка данных из json файла
with open('task_3_item.json', 'r') as f:
    additional_data = json.load(f)

# Добавление данных к существующей коллекции
collection.insert_many(additional_data)

# Запрос 11: удалить из коллекции документы по предикату: salary < 25 000 || salary > 175000
query11 = {"salary": {"$lt": 25000} or {"salary": {"$gt": 175000}}}
collection.delete_many(query11)
print("\nQuery 11: Deleted documents with salary < 25,000 or salary > 175,000")

# Запрос 12: увеличить возраст (age) всех документов на 1
query12 = {}
update12 = {"$inc": {"age": 1}}
collection.update_many(query12, update12)
print("\nQuery 12: Increased age of all documents by 1")

# Запрос 13: поднять заработную плату на 5% для произвольно выбранных профессий
query13 = {"job": {"$in": ["Профессия1", "Профессия2"]}}  # Замените на ваши профессии
update13 = {"$mul": {"salary": 1.05}}
collection.update_many(query13, update13)
print("\nQuery 13: Increased salary by 5% for selected professions")

# Запрос 14: поднять заработную плату на 7% для произвольно выбранных городов
query14 = {"city": {"$in": ["Город1", "Город2"]}}  # Замените на ваши города
update14 = {"$mul": {"salary": 1.07}}
collection.update_many(query14, update14)
print("\nQuery 14: Increased salary by 7% for selected cities")

# Запрос 15: поднять заработную плату на 10% для выборки по сложному предикату
# (произвольный город, произвольный набор профессий, произвольный диапазон возраста)
query15 = {
    "city": {"$in": ["Город3", "Город4"]},  # Замените на ваши города
    "job": {"$in": ["Профессия3", "Профессия4"]},  # Замените на ваши профессии
    "age": {"$gte": 25, "$lte": 35}  # Замените на ваш диапазон возраста
}
update15 = {"$mul": {"salary": 1.1}}
collection.update_many(query15, update15)
print("\nQuery 15: Increased salary by 10% for a complex query")

# Запрос 16: удалить из коллекции записи по произвольному предикату
query16 = {"age": {"$gt": 60}}  # Пример: удалить записи с возрастом больше 60 лет
collection.delete_many(query16)
print("\nQuery 16: Deleted documents with age greater than 60")

# Закрытие соединения с MongoDB
client.close()
