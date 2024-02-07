import os
import json
import xml.etree.ElementTree as ET
from statistics import mean, stdev

def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    objects_data = []
    
    for obj in root.findall('clothing'):
        obj_data = {}
        for attr in obj:
            tag = attr.tag.strip()
            text = attr.text.strip()
            
            # Приводим числовые значения к числовому формату
            if text.isdigit():
                text = int(text)
            elif '.' in text and text.replace('.', '').isdigit():
                text = float(text)
            
            obj_data[tag] = text
        
        objects_data.append(obj_data)
    
    return objects_data

def write_to_json(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)

# Папка с XML файлами
xml_folder = "xml_files"

# Список для хранения данных из всех файлов
all_data = []

# Парсинг XML файлов
for file_name in os.listdir(xml_folder):
    if file_name.endswith(".xml"):
        file_path = os.path.join(xml_folder, file_name)
        data = parse_xml(file_path)
        all_data.extend(data)

# Запись данных в JSON файл
write_to_json(all_data, "parsed_data.json")

# Отсортировать значения по полю "price"
sorted_data = sorted(all_data, key=lambda x: x.get('price', 0))

# Выполнить фильтрацию по полю "exclusive"
filtered_data = [item for item in all_data if item.get('exclusive') == 'no']

# Для числового поля "price" посчитать статистические характеристики
price_values = [item.get('price', 0) for item in all_data]
price_stats = {
    'Сумма': sum(price_values),
    'Минимальное значение': min(price_values),
    'Максимальное значение': max(price_values),
    'Среднее значение': mean(price_values),
    'Стандартное отклонение': stdev(price_values)
}

# Для текстового поля "category" посчитать частоту меток
category_labels_frequency = {}
for item in all_data:
    category_label = item.get('category', '')
    category_labels_frequency[category_label] = category_labels_frequency.get(category_label, 0) + 1

# Вывод результатов
print("Отсортированные данные по цене:")
print(sorted_data)

print("\nДанные после фильтрации по exclusive 'no':")
print(filtered_data)

print("\nСтатистические характеристики для поля 'price':")
print(price_stats)

print("\nЧастота меток для поля 'category':")
print(category_labels_frequency)
