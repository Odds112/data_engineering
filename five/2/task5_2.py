import pickle
from pymongo import MongoClient
import numpy as np

# Подключение к MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['task1DB']
collection = db['task1Coll']

# Загрузка данных из msgpack файла
with open('task_2_item.msgpack', 'rb') as f:
    additional_data = pickle.load(f)

# Добавление данных к существующей коллекции
collection.insert_many(additional_data)

# Запрос 1: вывод минимальной, средней, максимальной salary
query1 = collection.aggregate([
    {"$group": {"_id": None, "min_salary": {"$min": "$salary"}, "avg_salary": {"$avg": "$salary"}, "max_salary": {"$max": "$salary"}}}
])
result1 = list(query1)
print("Query 1:")
print(result1)

# Запрос 2: вывод количества данных по представленным профессиям
query2 = collection.aggregate([
    {"$group": {"_id": "$job", "count": {"$sum": 1}}}
])
result2 = list(query2)
print("\nQuery 2:")
print(result2)

# Запрос 3: вывод минимальной, средней, максимальной salary по городу
query3 = collection.aggregate([
    {"$group": {"_id": "$city", "min_salary": {"$min": "$salary"}, "avg_salary": {"$avg": "$salary"}, "max_salary": {"$max": "$salary"}}}
])
result3 = list(query3)
print("\nQuery 3:")
print(result3)

# Запрос 4: вывод минимальной, средней, максимальной salary по профессии
query4 = collection.aggregate([
    {"$group": {"_id": "$job", "min_salary": {"$min": "$salary"}, "avg_salary": {"$avg": "$salary"}, "max_salary": {"$max": "$salary"}}}
])
result4 = list(query4)
print("\nQuery 4:")
print(result4)

# Запрос 5: вывод минимального, среднего, максимального возраста по городу
query5 = collection.aggregate([
    {"$group": {"_id": "$city", "min_age": {"$min": "$age"}, "avg_age": {"$avg": "$age"}, "max_age": {"$max": "$age"}}}
])
result5 = list(query5)
print("\nQuery 5:")
print(result5)

# Запрос 6: вывод минимального, среднего, максимального возраста по профессии
query6 = collection.aggregate([
    {"$group": {"_id": "$job", "min_age": {"$min": "$age"}, "avg_age": {"$avg": "$age"}, "max_age": {"$max": "$age"}}}
])
result6 = list(query6)
print("\nQuery 6:")
print(result6)

# Запрос 7: вывод максимальной заработной платы при минимальном возрасте
query7 = collection.aggregate([
    {"$group": {"_id": None, "max_salary_at_min_age": {"$max": "$salary"}}}
])
result7 = list(query7)
print("\nQuery 7:")
print(result7)

# Запрос 8: вывод минимальной заработной платы при максимальном возрасте
query8 = collection.aggregate([
    {"$group": {"_id": None, "min_salary_at_max_age": {"$min": "$salary"}}}
])
result8 = list(query8)
print("\nQuery 8:")
print(result8)

# Запрос 9: вывод минимального, среднего, максимального возраста по городу, при условии, что заработная плата больше 50 000, отсортировать вывод по любому полю
query9 = collection.aggregate([
    {"$match": {"salary": {"$gt": 50000}}},
    {"$group": {"_id": "$city", "min_age": {"$min": "$age"}, "avg_age": {"$avg": "$age"}, "max_age": {"$max": "$age"}}},
    {"$sort": {"_id": 1}}  # Сортировка по возрастанию по полю _id (город)
])
result9 = list(query9)
print("\nQuery 9:")
print(result9)

# Запрос 10: вывод минимальной, средней, максимальной salary в произвольно заданных диапазонах по городу, профессии, и возрасту: 18 < age < 25 & 50 < age < 65
query10 = collection.aggregate([
    {"$match": {"$and": [{"age": {"$gt": 18, "$lt": 25}}, {"$or": [{"age": {"$gt": 50, "$lt": 65}}]}]}},
    {"$group": {"_id": {"city": "$city", "job": "$job"}, "min_salary": {"$min": "$salary"}, "avg_salary": {"$avg": "$salary"}, "max_salary": {"$max": "$salary"}}}
])
result10 = list(query10)
print("\nQuery 10:")
print(result10)

# Произвольный запрос с $match, $group, $sort
# Например, вывод средней зарплаты по городам, где средний возраст больше 30, с сортировкой по средней зарплате
custom_query = collection.aggregate([
    {"$group": {"_id": "$city", "avg_salary": {"$avg": "$salary"}, "avg_age": {"$avg": "$age"}}},
    {"$match": {"avg_age": {"$gt": 30}}},
    {"$sort": {"avg_salary": -1}}
])
custom_result = list(custom_query)
print("\nCustom Query:")
print(custom_result)

# Закрытие соединения с MongoDB
client.close()
