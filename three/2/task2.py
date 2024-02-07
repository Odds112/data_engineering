from bs4 import BeautifulSoup
import os
import json
from statistics import mean, stdev

def parse_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        
        objects_data = []
        
        product_items = soup.find_all('div', class_='product-item')
        for item in product_items:
            obj_data = {
                'ID': item.find('a', class_='add-to-favorite')['data-id'],
                'Image': item.find('div').find('img')['src'],
                'Title': item.find('span').get_text(strip=True),
                'Price': item.find('price').get_text(strip=True),
                'BonusInfo': item.find('strong').get_text(strip=True),
                'Characteristics': [li.get_text(strip=True) for li in item.find('ul').find_all('li')]
            }
            objects_data.append(obj_data)
        
        return objects_data

def write_to_json(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)

# Папка с HTML файлами
html_folder = "html_files"

# Список для хранения данных из всех файлов
all_data = []

# Парсинг HTML файлов
for file_name in os.listdir(html_folder):
    if file_name.endswith(".html"):
        file_path = os.path.join(html_folder, file_name)
        data = parse_html(file_path)
        all_data.extend(data)

# Запись данных в JSON файл
write_to_json(all_data, "parsed_data.json")

# Отсортировать значения по полю "Title"
sorted_data = sorted(all_data, key=lambda x: x['Title'])

# Выполнить фильтрацию по полю "Price"
filtered_data = [item for item in all_data if '415 140' in item['Price']]

# Для числового поля "ID" посчитать статистические характеристики
id_values = [int(item['ID']) for item in all_data]
id_stats = {
    'Сумма': sum(id_values),
    'Минимальное значение': min(id_values),
    'Максимальное значение': max(id_values),
    'Среднее значение': mean(id_values),
    'Стандартное отклонение': stdev(id_values)
}

# Для текстового поля "Title" посчитать частоту меток
title_labels_frequency = {}
for item in all_data:
    title_label = item['Title']
    title_labels_frequency[title_label] = title_labels_frequency.get(title_label, 0) + 1

# Вывод результатов
print("Отсортированные данные по названию:")
print(sorted_data)

print("\nДанные после фильтрации по цене 415 140 ₽:")
print(filtered_data)

print("\nСтатистические характеристики для поля 'ID':")
print(id_stats)

print("\nЧастота меток для поля 'Title':")
print(title_labels_frequency)
