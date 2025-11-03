import csv
import sqlite3
import datetime

now_data = datetime.datetime.utcnow().strftime("%H:%M-%d.%m.%Y")

class SQL_atm:

    @staticmethod
    def create_table():
        """Создание таблицы Users_data"""

        with sqlite3.connect("atm.db") as db:
            cur = db.cursor()
            cur.execute("""
                        CREATE TABLE IF NOT EXISTS Users_data(
                        UserID INTEGER PRIMARY KEY AUTOINCREMENT,
                        Number_card INTEGER UNIQUE NOT NULL,
                        Pin_code INTEGER NOT NULL,
                        Balance INTEGER NOT NULL);
                        """)
            print("Таблица Users_data доступна к работе")

    @staticmethod
    def insert_users(data_users):
        """Создание нового пользователя в Users_data"""

        with sqlite3.connect("atm.db") as db:
            cur = db.cursor()
            cur.execute("""INSERT OR IGNORE INTO  Users_data (Number_card, Pin_code, Balance) VALUES(?, ?, ?);""", data_users)
            if cur.rowcount > 0:
                print("Создание нового пользователя")
                return True
            else:
                return False

    @staticmethod
    def input_card(number_card):
        """Ввод и проверка карты"""

        try:
            with sqlite3.connect("atm.db") as db:
                cur = db.cursor()
                cur.execute(f"""SELECT Number_card FROM Users_data WHERE Number_card = {number_card}""")
                result_card = cur.fetchone()
                if result_card == None:
                    print('Введен неизвестный номер карты')
                    return False
                else:
                    print(f'Введен номер карты: {number_card}')
                    return True
        except:
            print("Ошибка: введен некорректный номер карты")

    @staticmethod
    def input_code(number_card):
        """Ввод и проверка пин-код"""

        pin_code = input("Введите, пожалуйста, пин-код карты: ")
        with sqlite3.connect("atm.db") as db:
            cur = db.cursor()
            cur.execute(f"""
                SELECT Pin_code 
                FROM Users_data 
                WHERE Number_card = {number_card}
            """)
            result_code = cur.fetchone()
            input_pin = result_code[0] # значение пин-кода
            try:
                if input_pin == int(pin_code):
                    print("Введен верный пин-код")
                    return True
                else:
                    return False
            except:
                print('Ошибка: Введен некорректный пин-код')

    @staticmethod
    def info_balance(number_card):
        """Вывод на экран баланса карты"""

        with sqlite3.connect("atm.db") as db:
            cur = db.cursor()
            cur.execute(f"""
                SELECT Balance 
                FROM Users_data 
                WHERE Number_card = {number_card};
            """)
            result_info_balance = cur.fetchone()
            balance_card = result_info_balance[0]
            print(f"Баланс вашей карты: {balance_card}")

    @staticmethod
    def withdraw_money(number_card):
        """Снятие денежных средств с баланса карты"""
        
        amount = input('Введите желаемую сумму для снятия: ')
        with sqlite3.connect("atm.db") as db:
            cur = db.cursor()
            cur.execute(f"""
                SELECT Balance 
                FROM Users_data 
                WHERE Number_card = {number_card};
            """)
            result_info_balance = cur.fetchone()
            balance_card = result_info_balance[0]
            try:
                if int(amount) > balance_card:
                    print("Ошибка: Недостаточно средств")
                    return  False
                elif int(amount) < 0:
                    print('Нельзя вводить отрицательное число')
                    return False
                else:
                    cur.execute(f"""
                                    UPDATE Users_data 
                                    SET Balance = Balance - {amount} 
                                    WHERE Number_card = {number_card};
                    """)
                    db.commit()
                    SQL_atm.info_balance(number_card)
                    SQL_atm.report_operation_1(now_data, number_card, "1", amount, "")
                    return True
            except:
                print('Некорректное действие. Повторите попытку.')
                return False

    @staticmethod
    def depositing_money(number_card):
        """Внесение денежных средств"""
        
        amount = input('Введите сумму пополнения: ')
        with sqlite3.connect("atm.db") as db:
            cur = db.cursor()
            try:
                if int(amount) < 0:
                    print("Нельзя вводить отрицательное число")
                    raise Exception
                cur.execute(
                    f"""
                    UPDATE Users_data
                    SET Balance = Balance + {amount}
                    WHERE Number_card = {number_card}; 
                    """
                )
                db.commit()
                SQL_atm.info_balance(number_card)
                SQL_atm.report_operation_1(now_data, number_card, "2", amount, "")
            except:
                print('Некорректное действие. Повторите попытку.')
                return False
    
    @staticmethod
    def transfer_money(number_card):
        """Перевод денежных средств на другую карту"""
        
        amount = input('Введите сумму для перевода: ')
        with sqlite3.connect("atm.db") as db:
            cur = db.cursor()
            cur.execute(f"""
                SELECT Balance 
                FROM Users_data 
                WHERE Number_card = {number_card};
            """)
            result_info_balance = cur.fetchone()
            balance_card = result_info_balance[0]
            try:
                if int(amount) < 0:
                    print("Нельзя вводить отрицательное число")
                    raise Exception
                elif int(amount) > balance_card:
                    print("Ошибка: Недостаточно средств")
                    return  False
                else:
                    target_card = input("Введите номер карты получателя: ")
                    if target_card == number_card:
                        print("Ошибка: Нельзя сделать перевод на свою карту.")
                        return False
                    SQL_atm.input_card(target_card)
                    cur = db.cursor()
                    cur.execute(
                        f"""
                        UPDATE Users_data
                        SET Balance = Balance - {amount}
                        WHERE Number_card = {number_card}               
                        """
                    )
                    db.commit()
                    cur.execute(
                        f"""
                        UPDATE Users_data
                        SET Balance = Balance + {amount}
                        WHERE Number_card = {target_card}
                        """
                    )
                    db.commit()
                    SQL_atm.info_balance(number_card)
                    SQL_atm.report_operation_1(now_data, number_card, "3", amount, target_card)
                    SQL_atm.report_operation_2(now_data, target_card, "3", amount, number_card)
            except:
                print('Некорректное действие. Повторите попытку снова.')
                return False

    @staticmethod
    def input_operation(number_card):
        """Выбор операции"""
        
        while True:
            operation = input("Выберете операцию:\n"
                            "1. Узнать баланс\n"
                            "2. Снять денежные средства\n"
                            "3. Внести денежные средства\n"
                            "4. Завершить работу\n"
                            "5. Перевести денежные средства\n")
            match operation:
                case "1":
                    SQL_atm.info_balance(number_card)
                case "2":
                    SQL_atm.withdraw_money(number_card)
                case "3":
                    SQL_atm.depositing_money(number_card)
                case "4":
                    print("Спасибо за ваш визит, всего доброго!")
                    return False
                case "5":
                    SQL_atm.transfer_money(number_card)
                case _:
                    print("Ошибка: операция недоступна. Попробуйте другую операцию.")

    @staticmethod
    def report_operation_1(now_data, number_card, type_operation, amount, payee):
        """Отчеты транзакций"""
        
        """
        Type_operation
        1 - Снятие денежных средств
        2 - Пополнение счета
        3 - Перевод денежных средств
        """
        # Data;Number_card;Type_operation;Amount;Payee
        user_data = [
            (now_data, number_card, type_operation, amount, payee)
        ]

        with open("report_1.csv", "a", newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerows(
                user_data
            )
        print('Данные внесены в отчет')
        
    @staticmethod
    def report_operation_2(now_data, payee, type_operation, amount, sender):
        """Отчеты транзакций"""
        
        """
        Type_operation
        1 - Снятие денежных средств
        2 - Пополнение счета
        3 - Перевод денежных средств
        """
        # Data;Payee;Type_operation;Amount;Sender
        user_data = [
            (now_data, payee, type_operation, amount, sender)
        ]

        with open("report_2.csv", "a", newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerows(
                user_data
            )
        print('Данные внесены в отчет')
