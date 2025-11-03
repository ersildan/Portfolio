s = list(input())
for i, el in enumerate(s, 1):
    print(i, end='') if el == '#' else print(el, end='')
