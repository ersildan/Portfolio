import sys

mail_data = {'address': 'test@test.ru', 'subject': 'Спец.письмо', 'text': 'Царский указ'}

lst = [line.strip() for line in sys.stdin]

if lst[0] is None or lst[1] is None:
    print('Bad')
elif lst[0] != mail_data['address'] or lst[1] != mail_data['subject']:
    print('Bad')
else:
    print('Good')
