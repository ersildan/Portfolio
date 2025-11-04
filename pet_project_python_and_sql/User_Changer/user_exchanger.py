import sqlite3

"""Создаем базу данных users_balance"""

db = sqlite3.connect('exchanger.db')
cur = db.cursor()

cur.execute("""
            CREATE TABLE IF NOT EXISTS users_balance(
            UserID TEXT PRIMARY KEY,
            Balance_RUB FLOAT NOT NULL,
            Balance_USD FLOAT NOT NULL,
            Balance_EUR FLOAT NOT NULL);
            """)

print("\033[32mДобро пожаловать в обменник валют\033[0m")

"""Вносим первого пользователя в таблицу.
Безопасным способом от SQL-инъекций.
Игнорируем вставку, если он уже есть."""

money_params = ('Брюс Уэйн', 1000000.0, 1000.0, 100.0)
cur.execute("""
            INSERT OR IGNORE INTO users_balance 
            (UserID, Balance_RUB, Balance_USD, Balance_EUR)
            VALUES (?, ?, ?, ?)
            """, money_params)
db.commit()

exc_txt =   """
            Курс валют:
            1 USD = 70 RUB
            1 EUR = 80 RUB
            1 USD = 0,87 EUR
            1 EUR = 1,15 USD
            """

d = {
     '1': 'RUB',
     '2': 'USD',
     '3': 'EUR'
}

def update_balance(amount, choice_1, choice_2, balance, name_exc):
    """Функция для обновления данных в users_balance"""

    code = choice_1 + choice_2 # Ключ для словаря dict_code
    dict_code = {
         '12': 1/70, '13': 1/80,
         '21': 70, '23': 0.87,
         '31': 80, '32': 1.15
    }

    update_amount = amount * dict_code[code] # Сумма на которую увеличим старый баланс
    new_balance = balance - amount  # Баланс первой валюты, которую отдали для обмена
    name_exc_ = 'Balance_' + d[choice_2] # Имя валюты у которой пополнили баланс при обмене

    print(f'Совершен обмен валют {amount} {d[choice_1]} на {round(update_amount, 2)} {d[choice_2]}')

   # Обновляем users_balance новыми данными
    cur.executescript(  f"""
                        UPDATE users_balance SET {name_exc} = {new_balance};
                        UPDATE users_balance SET {name_exc_} =  {name_exc_} + {update_amount}
                        """)
    db.commit()

def check_amount(amount, choice_1):
    """Проверка amount на правильность ввода и на остаток баланса"""

    try:
        amount = float(amount.replace(',', '.')) # Проверка числа на float()
        if amount == 0:
            raise Exception
    except:
        raise Exception ('\033[31mОшибка\033[0m: Нужно вводить только цифры больше нуля')

    cur.execute("""SELECT * FROM users_balance limit 1;""")

    data = cur.fetchone() # Данные из строки в таблице users_balance
    balance = data[int(choice_1)] # Баланс выбранной валюты
    name_exc = cur.description[int(choice_1)][0] # Наименование валюты

    if amount > balance:
        raise Exception (f'\033[31mНедостаточно средств\033[0m: {name_exc} = {balance}\n'
                         'Повторите попытку')
    if amount < 0:
        raise Exception('\033[31mОшибка\033[0m: Число не должно быть отрицательным')

    print(*[f"\033[93mВведите [ {key} ] для обмена на {d[key]}\033[0m"
           for key, value in d.items() if key != choice_1], sep='\n') # Выводим список доступных валют для обмена

    choice_2 = input() # Выбор пользователя на что он будет менять свою валюту

    if choice_2.isdigit() is not True:
        raise Exception('\033[31mОшибка\033[0m: Нужно вводить только положительное число без букв')
    if choice_1 == choice_2 or choice_2 not in ['1', '2', '3']:
        raise Exception('\033[31mОшибка\033[0m: Выбирайте, пожалуйста, из доступных вариантов')

    update_balance(amount, choice_1, choice_2, balance, name_exc)

    cur.execute("""SELECT * FROM users_balance limit 1;""")
    new_data = cur.fetchone() # Берем первую строку из таблицы users_balance

    b1 = new_data[int(choice_1)] # Баланс валюты, которую отдали
    b2 = new_data[int(choice_2)] # Баланс валюты, которую пополнили

    print(f"Баланс {d[choice_1]} = {round(b1, 2)}\nБаланс {d[choice_2]} = {round(b2, 2)}")
    print('Программа успешно завершена.')

def func():
    """Выбираем валюту для обмена"""

    while True:
        try:
            txt = ("\033[93mВведите [ 1 ] если хотите обменять RUB\n"
                   "Введите [ 2 ] если хотите обменять USD\n"
                   "Введите [ 3 ] если хотите обменять EUR\n"
                   "Введите [ 4 ] чтобы вывести курс валют\033[0m\n"
                   "Чтобы \033[31mвыйти\033[0m введите любой символ")
            print(txt)

            choice_1 = input() # Выбор валюты от пользователя согласно тексту в txt

            match choice_1:
                case '1':
                    print('Сколько желаете обменять RUB?')
                case '2':
                    print('Сколько желаете обменять USD?')
                case '3':
                    print('Сколько желаете обменять EUR?')
                case '4':
                    print(exc_txt)
                    raise Exception
                case _:
                    exit('Совершен выход из обменника')

            amount = input() # Желаемая сумма для обмена на другую валюту
            check_amount(amount, choice_1) # Проверка введенной суммы (amount)

            break
        except Exception as e:
            print(e)

if __name__ == '__main__':
    func()
