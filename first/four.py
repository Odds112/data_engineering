import csv
from operator import itemgetter

# Имя входного и выходного файлов
input_file = 'text_4_var_30.csv'
output_file = 'output.csv'
name_line = ['id', 'имя', 'фамилия', 'age', 'salary', 'номер телефона']

# Чтение данных из CSV файла
with open(input_file, 'r', newline='', encoding='utf-8') as file_input:
    reader = csv.DictReader(file_input, fieldnames=name_line)
    data = list(reader)

# 1. Удаление колонки с номером телефона
for x in data:
    del x['номер телефона']
    x['salary'] = x['salary'].replace('₽', '')
    x['name'] = x.pop('имя') + ' ' + x.pop('фамилия')

# 2. Рассчет среднего дохода и фильтрация строк
avg = sum(float(x['salary']) for x in data) / len(data)
data = [x for x in data if float(x['salary']) >= avg]

for x in data:
    x['salary'] = x['salary'] + "₽"
# 3. Применение фильтра по возрасту (оставляем строки со значением возраста более 25)
data = [x for x in data if int(x['age']) > 25]

# Сортировка данных по полю 'порядковый номер' (по возрастанию)
data = sorted(data, key=itemgetter('id'))

# Запись полученных результатов в новый CSV файл
fieldNames = ['id', 'name', 'age', 'salary']
with open(output_file, 'w', newline='', encoding='utf-8') as file_out:
    reader = csv.DictWriter(file_out, fieldnames=fieldNames)
    reader.writeheader()
    reader.writerows(data)
