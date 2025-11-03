hour, minutes = input().split(':')
if int(hour) <= 12:
    print(f"am - {hour}:{minutes}")
else:
    print(f"pm - {int(hour) - 12}:{minutes}")
    