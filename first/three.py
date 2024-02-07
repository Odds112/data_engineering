import math

input_file = 'text_3_var_30.txt'
output_file = 'output.txt'

def data_proc(input, output):
    with open(input, 'r') as file_in, open(output, 'w') as file_out:
        for line in file_in:
            # Заменяем "NA" средним значением соседних чисел
            nums = [float(num) if num != "NA" else None for num in line.split(",")]
            for i in range(len(nums)):
                if nums[i] is None:
                    # Рассчитываем среднее значение соседних чисел
                    num_near = [число for число in (nums[i - 1], nums[i + 1]) if число is not None]
                    if num_near:
                        nums[i] = sum(num_near) / len(num_near)

            # Фильтруем значения, исключая те, корень квадратный из которых меньше 80
            fillter_nums = [num for num in nums if num is not None and math.sqrt(num) >= 80]

            # Записываем результат в выходной файл
            line_result = ' '.join(map(str, fillter_nums))
            file_out.write(line_result + '\n')

data_proc(input_file, output_file)
