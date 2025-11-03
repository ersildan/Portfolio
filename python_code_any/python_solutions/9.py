from datetime import datetime as dt

day = dt.strptime(input(), '%d.%m.%Y').date()
print(dt.strftime(day, '%d.%m.%Y'))
