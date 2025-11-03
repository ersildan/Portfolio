v1, v2 = input(), input()

for letter in v1:
    if letter in v2:
        print('Good')
        break
else:
    print('Bad')
    