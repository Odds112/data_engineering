import re
from collections import Counter

f = open('text_1_var_30.txt', 'r')
t = f.read()
t = re.split(";|,|\n| |!|\.|\?", t)
t = list(filter(None, t)) # убрать пустые строки
text = ' '.join(t)
freq = Counter(text.split())
sort_freq = freq.most_common()
for word, fr in sort_freq:
    print(f"{word}: {fr}")
