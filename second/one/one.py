import numpy as np
import json

# Загрузка матрицы из файла
matrix = np.load('matrix_30.npy')

# Преобразование типа данных элементов матрицы в int
matrix = matrix.astype(int)

# Подсчет суммы и среднего арифметического всех элементов матрицы
total_sum = np.sum(matrix)
total_avr = np.mean(matrix)

# Подсчет суммы и среднего арифметического главной диагонали
main_diag_sum = np.trace(matrix)
main_diag_avr = np.mean(np.diag(matrix))

# Подсчет суммы и среднего арифметического побочной диагонали
side_diag_sum = np.trace(np.fliplr(matrix))
side_diag_avr = np.mean(np.fliplr(matrix).diagonal())

# Нахождение максимального и минимального значений
max_val = np.max(matrix)
min_val = np.min(matrix)

# Нормализация матрицы
normalized_matrix = (matrix - np.min(matrix)) / (np.max(matrix) - np.min(matrix))

# Сохранение нормализованной матрицы в формате npy
np.save('normalized_matrix.npy', normalized_matrix)

# Подготовка данных для записи в JSON
output_data = {
    'sum': int(total_sum),
    'avr': float(total_avr),
    'sumMD': int(main_diag_sum),
    'avrMD': float(main_diag_avr),
    'sumSD': int(side_diag_sum),
    'avrSD': float(side_diag_avr),
    'max': int(max_val),
    'min': int(min_val)
}

# Запись данных в JSON файл
with open('outData.json', 'w') as json_file:
    json.dump(output_data, json_file, indent=4)
