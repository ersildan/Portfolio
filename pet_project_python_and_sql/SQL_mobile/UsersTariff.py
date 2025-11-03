import sqlite3

class UsersTariff:

    @staticmethod
    def create_table():
        """
        Создание БД mobile.db
        создание таблиц: mobile_users, mobile_tariff
        """

        with sqlite3.connect("mobile.db") as db:
            cur = db.cursor()
            cur.execute("""
                        CREATE TABLE IF NOT EXISTS mobile_users(
                        UserID INTEGER PRIMARY KEY AUTOINCREMENT,
                        User_name TEXT UNIQUE NOT NULL,
                        Balance INTEGER NOT NULL,
                        Mobile_tariff_ref INTEGER NOT NULL,
                        Activity TEXT NOT NULL);
                        """)
            cur.execute("""
                        CREATE TABLE IF NOT EXISTS mobile_tariff(
                        TariffID INTEGER PRIMARY KEY AUTOINCREMENT,
                        Tariff TEXT UNIQUE NOT NULL,
                        Price INTEGER NOT NULL);
                        """)
            print("Таблицы mobile_users, mobile_tariff доступны к работе.")
    
    @staticmethod
    def insert_users(data_user):
        """Добавление нового пользователя в mobile_users"""
    
        with sqlite3.connect("mobile.db") as db:
            cur = db.cursor()
            cur.execute("""
                        INSERT OR IGNORE INTO mobile_users 
                        (User_name, Balance, Mobile_tariff_ref, Activity)
                        VALUES (?, ?, ?, ?);
                        """, data_user)
            if cur.rowcount > 0:
                print("Создание нового пользователя")
                return True
            else:
                return False
    
    @staticmethod
    def insert_tariff(data_tariff):
        """Добавление нового тарифа в mobile_tariff"""

        with sqlite3.connect("mobile.db") as db:
            cur = db.cursor()
            cur.execute("""
                        INSERT OR IGNORE INTO mobile_tariff
                        (Tariff, Price)
                        VALUES (?, ?)
                        """, data_tariff)
            if cur.rowcount > 0:
                print("Создание нового тарифа")
                return True
            else:
                return False
    
    @staticmethod
    def check_balance(num_month):
        """Проверяем баланс и статус клиента"""

        with sqlite3.connect("mobile.db") as db:
            cur = db.cursor()
            cur.execute("""
            SELECT u.User_name, u.Balance, t.Price, u.Activity
            FROM mobile_users u
            INNER JOIN mobile_tariff t 
                        ON u.Mobile_tariff_ref = t.TariffID
            WHERE u.Activity = 'Yes';
            """)

            result_code = cur.fetchall() # Сохраняем нужные данные из двух таблиц после INNER JOIN
           
            for user_info in result_code:
                # Пробегаем по каждому пользователю и его данным

                name, balance, tariff, status = user_info # Задаю переменные для удобства
                
                if balance > tariff and status == 'Yes':
                    cur = db.cursor()
                    cur.execute(f"""
                                UPDATE mobile_users
                                SET Balance = Balance - {tariff}
                                WHERE User_name = '{name}'
                                """)
                    db.commit()
                    print(f"{name} снятие денежных средств {tariff} за месяц №{num_month}")
                else:
                    cur.execute(f"""
                                UPDATE mobile_users
                                SET Activity = 'No'
                                WHERE User_name = '{name}'
                                """)
                    db.commit()
                    print(f"{name} недостаточно средств на балансе")
