data = {'a': 1, 'b': 2, 'c': 3}
key = input()
if key in data:
    del data[key]
print(*[f"{k} - {v}" for k,v in data.items()], sep='\n')