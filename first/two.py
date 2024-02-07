def find_sum(line):
    nums = [int(x) for x in line.split() if x.isdigit()]
    sum_nums = sum(nums)
    print(sum_nums)

f = open('text_2_var_30.txt', 'r')
t = f.read()
t = t.split("\n")
for line in t:
   find_sum(line)
