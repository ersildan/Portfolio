lst = [el for el in input() if el.isdigit() == True ]

lst[0] = '+7 ('
lst[3] = lst[3] + ') '
lst[6] = lst[6] + '-'
lst[8] = lst[8] + '-'

print(''.join(lst))
