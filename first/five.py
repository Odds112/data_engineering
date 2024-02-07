from bs4 import BeautifulSoup
import csv

# Имя входного и выходного файлов
input_html = 'text_5_var_30.html'
out_csv = 'outputDataHtml.csv'

# Чтение данных из HTML файла
with open(input_html, 'r', encoding='utf-8') as file_html:
    data_html = file_html.read()

# Извлечение данных из таблицы HTML
soup = BeautifulSoup(data_html, 'html.parser')
tab = soup.find('table')

# Подготовка данных для записи в CSV
data = []
header = [th.text.strip() for th in tab.find_all('th')]
data.append(header)

for line in tab.find_all('tr')[1:]:
    x = [td.text.strip() for td in line.find_all('td')]
    data.append(x)

# Запись данных в CSV файл
with open(out_csv, 'w', newline='', encoding='utf-8') as file_csv:
    reader = csv.writer(file_csv)
    reader.writerows(data)
