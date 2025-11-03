from UsersTariff import UsersTariff


class MobileTariff:

    def MobileTariff_logic(self):

        # Создаем БД и таблицы 
        UsersTariff.create_table()
        
        # Наполняем таблицу mobile_users
        UsersTariff.insert_users(("User1", 10000, 2, "Yes"))
        UsersTariff.insert_users(("User2", 10000, 3, "Yes"))
        UsersTariff.insert_users(("User3", 10000, 3, "Yes"))
        
        # Наполняем таблицу mobile_tariff
        UsersTariff.insert_tariff(("Standart", 500))
        UsersTariff.insert_tariff(("VIP", 1000))
        UsersTariff.insert_tariff(("Premium", 1500))

        n = int(input("Введите период расчета: "))

        for num_month in range(1, n + 1):
            UsersTariff.check_balance(num_month)
            print()

start = MobileTariff()
start.MobileTariff_logic()
