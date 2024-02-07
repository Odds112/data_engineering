import pickle
from pymongo import MongoClient

# Подключение к MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['task1DB']
collection = db['task1Coll']

# Загрузка данных из pkl файла
with open('task_1_item.pkl', 'rb') as f:
    data = pickle.load(f)

# Запись данных в MongoDB
collection.insert_many(data)

# Задайте произвольные значения для переменных
VAR = 10

# Вывод первых 10 записей, отсортированных по убыванию по полю salary
query1 = collection.find().sort('salary', -1).limit(VAR)
result1 = list(query1)
print("Query 1:")
print(result1)

# Вывод первых 15 записей, отфильтрованных по предикату age < 30, отсортированных по убыванию по полю salary
query2 = collection.find({'age': {'$lt': 30}}).sort('salary', -1).limit(15)
result2 = list(query2)
print("\nQuery 2:")
print(result2)

# Вывод первых 10 записей, отфильтрованных по сложному предикату и отсортированных по возрастанию по полю age
city_filter = 'Кишинев'  # Ваш произвольный город
professions_filter = ['Архитектор', 'Профессия_2', 'Профессия_3']  # Ваши произвольные профессии

query3 = collection.find({
    'city': city_filter,
    'job': {'$in': professions_filter}
}).sort('age', 1).limit(VAR)
result3 = list(query3)
print("\nQuery 3:")
print(result3)

# Вывод количества записей, получаемых в результате фильтрации
query4 = collection.find({
    'age': {'$gte': 30, '$lte': 40},
    'year': {'$in': list(range(2019, 2023))},
    '$or': [
        {'salary': {'$gt': 50000, '$lte': 75000}},
        {'$and': [{'salary': {'$gt': 125000}}, {'salary': {'$lt': 150000}}]}
    ]
}).count()
print("\nQuery 4:")
print(f"Count: {query4}")

# Закрытие соединения с MongoDB
client.close()

