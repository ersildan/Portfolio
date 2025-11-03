s = input().split()
for el in s:
    if el[0].isalpha() == False and el[1] in ('.',')'):
        print(el)
