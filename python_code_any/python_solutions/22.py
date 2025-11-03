n = int(input())
if n < 10000:
    print(*[n, 0], sep='\n')
else:
    print(*[int(n * 0.7), int(n * 0.3)], sep='\n')
    