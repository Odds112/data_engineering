import numpy as np

# Загрузка матрицы из файла
matrix = np.load('matrix_30_2.npy')

# Определение условия для фильтрации
value = 530

# Фильтрация матрицы и получение индексов и значений
indices_x, indices_y = np.where(matrix > value)
values_z = matrix[indices_x, indices_y]

# Создание массивов x, y, z
array_x = np.array(indices_x)
array_y = np.array(indices_y)
array_z = np.array(values_z)

# Сохранение массивов в формате npz
np.savez('out_data.npz', x=array_x, y=array_y, z=array_z)

# Сохранение массивов в сжатом формате npz
np.savez_compressed('out_data_compressed.npz', x=array_x, y=array_y, z=array_z)
