n = int(input())

while n > 0:
    if n % 100 != 0 and n % 10 != 0 and n % 5 != 0:
        print('Bad')
        break 
    if n > 100:
        print(f"100 - {n // 100}")
        n = n - (n // 100) * 100
    if n <= 100:
        print(f"10 - {n // 10}")
        n = n - (n // 10) * 10
    if n <= 5 and n != 0:
        print(f"5 - {n // 5}")
        n = n - (n // 5) * 5
        