import os
import json
import xml.etree.ElementTree as ET
from statistics import mean, stdev

def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    obj_data = {}
    
    for child in root:
        tag = child.tag.strip()
        text = child.text.strip()
        
        # Приводим числовые значения к числовому формату
        if text.isdigit():
            text = int(text)
        elif '.' in text and text.replace('.', '').isdigit():
            text = float(text)
        
        obj_data[tag] = text
    
    return obj_data

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
        all_data.append(data)

# Запись данных в JSON файл
write_to_json(all_data, "parsed_data.json")

# Отсортировать значения по полю "radius"
sorted_data = sorted(all_data, key=lambda x: x.get('radius', 0))

# Выполнить фильтрацию по полю "spectral-class"
filtered_data = [item for item in all_data if item.get('spectral-class') == 'D4O']

# Для числового поля "radius" посчитать статистические характеристики
radius_values = [item.get('radius', 0) for item in all_data]
radius_stats = {
    'Сумма': sum(radius_values),
    'Минимальное значение': min(radius_values),
    'Максимальное значение': max(radius_values),
    'Среднее значение': mean(radius_values),
    'Стандартное отклонение': stdev(radius_values)
}

# Для текстового поля "name" посчитать частоту меток
name_labels_frequency = {}
for item in all_data:
    name_label = item.get('name', '')
    name_labels_frequency[name_label] = name_labels_frequency.get(name_label, 0) + 1

# Вывод результатов
print("Отсортированные данные по радиусу:")
print(sorted_data)

print("\nДанные после фильтрации по spectral-class 'D4O':")
print(filtered_data)

print("\nСтатистические характеристики для поля 'radius':")
print(radius_stats)

print("\nЧастота меток для поля 'name':")
print(name_labels_frequency)
