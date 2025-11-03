import datetime

h, m = map(int, input().split(':'))
s = int(input()) * 60
res = h * 60 * 60 + m * 60 + s


result_time = datetime.timedelta(seconds=res)
print(result_time)

#print(result_time.strftime('%H:%M'))
