import json
import msgpack

# Чтение массива объектов из файла json
with open('products_30.json', 'r') as json_file:
    products_data = json.load(json_file)

# Создание словаря для хранения информации о каждой группе
grouped_info = {}

# Группировка элементов по полю 'name'
for product in products_data:
    name = product['name']
    price = product['price']

    if name not in grouped_info:
        grouped_info[name] = {'average_price': 0, 'max_price': 0, 'min_price': float('inf')}

    if 'prices' not in grouped_info[name]:
        grouped_info[name]['prices'] = []

    grouped_info[name]['prices'].append(price)

# Нахождение средней, максимальной и минимальной цен для каждой группы
for name, info in grouped_info.items():
    prices = info['prices']
    average_price = sum(prices) / len(prices)
    max_price = max(prices)
    min_price = min(prices)

    info['average_price'] = average_price
    info['max_price'] = max_price
    info['min_price'] = min_price

    # Удаление массива 'prices'
    del info['prices']

# Сохранение информации в формате json
with open('product_info.json', 'w') as json_output:
    json.dump(grouped_info, json_output, indent=4)

# Сохранение информации в формате msgpack
with open('product_info.msgpack', 'wb') as msgpack_output:
    packed_data = msgpack.packb(grouped_info)
    msgpack_output.write(packed_data)
