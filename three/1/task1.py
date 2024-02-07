from bs4 import BeautifulSoup
import os
import json
from statistics import mean, stdev


# Функция для парсинга HTML и извлечения данных
def parse_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

        data = {
            'Тип': soup.find('span', text='Тип:').find_next('span').get_text(strip=True),
            'Турнир': soup.find('h1', class_='title').get_text(strip=True),
            'Город': soup.find('p', class_='address-p').find('span', text='Город:').find_next('span').get_text(
                strip=True),
            'Начало': soup.find('p', class_='address-p').find('span', text='Начало:').find_next('span').get_text(
                strip=True),
            'Количество туров': int(soup.find('span', class_='count').get_text(strip=True).split(':')[-1]),
            'Контроль времени': int(soup.find('span', class_='year').get_text(strip=True).split(':')[-1].split()[0]),
            'Минимальный рейтинг для участия': int(
                soup.find('span', text='Минимальный рейтинг для участия:').find_next('span').get_text(strip=True)),
            'Рейтинг': float(
                soup.find('div', class_='chess-wrapper').find_all('span')[0].get_text(strip=True).split(':')[-1]),
            'Просмотры': int(
                soup.find('div', class_='chess-wrapper').find_all('span')[1].get_text(strip=True).split(':')[-1]),
        }

        return data


# Папка с HTML файлами
html_folder = "html_files"

# Список для хранения данных из всех файлов
all_data = []

# Парсинг HTML файлов
for file_name in os.listdir(html_folder):
    if file_name.endswith(".html"):
        file_path = os.path.join(html_folder, file_name)
        data = parse_html(file_path)
        all_data.append(data)

# Запись данных в JSON файл
with open("parsed_data.json", "w", encoding="utf-8") as json_file:
    json.dump(all_data, json_file, ensure_ascii=False, indent=2)

# Отсортировать значения по полю "Рейтинг"
sorted_data = sorted(all_data, key=lambda x: x['Рейтинг'])

# Выполнить фильтрацию по полю "Тип"
filtered_data = [item for item in all_data if item['Тип'] == 'Swiss']

# Для числового поля "Просмотры" посчитать статистические характеристики
views_values = [item['Просмотры'] for item in all_data]
views_stats = {
    'Сумма': sum(views_values),
    'Минимальное значение': min(views_values),
    'Максимальное значение': max(views_values),
    'Среднее значение': mean(views_values),
    'Стандартное отклонение': stdev(views_values)
}

# Для текстового поля "Турнир" посчитать частоту меток
tournament_labels_frequency = {}
for item in all_data:
    tournament_label = item['Турнир']
    tournament_labels_frequency[tournament_label] = tournament_labels_frequency.get(tournament_label, 0) + 1

# Вывод результатов
print("Отсортированные данные по рейтингу:")
print(sorted_data)

print("\nДанные после фильтрации по типу 'Swiss':")
print(filtered_data)

print("\nСтатистические характеристики для поля 'Просмотры':")
print(views_stats)

print("\nЧастота меток для поля 'Турнир':")
print(tournament_labels_frequency)
