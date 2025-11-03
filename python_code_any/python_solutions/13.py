person_data = {'Login': 'User1',
               'Password': 'Qwer_1234'}
print(['Bad','Good'][person_data['Login'] == input() and person_data['Password'] == input()])