from datetime import timedelta as td

user_time, user_minutes = input(), int(input())

if user_minutes > 60:
    print('Bad')
else:
    u_hours, u_minutes = user_time.split(':')
    delta1 = td(hours= int(u_hours), minutes= int(u_minutes))
    delta2 = td(minutes = int(user_minutes))
    result = delta1 + delta2
    res = str(result)[-8:-3]
    print('0' + res[1:] if res[0] == ' ' else res)