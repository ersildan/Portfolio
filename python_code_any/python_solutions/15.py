data = {'a': 1, 'b': 0, 'c': 3, 'd': 0}
data = {k: v for k,v in data.items() if v != 0}
print(*[f"{k} - {v}" for k, v in data.items()], sep='\n')