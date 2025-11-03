import sqlite3

"""Задание по Регистрации пользователя"""

txt_choice = """Введите цифру [ 1 ] если хотите зарегистрировать нового пользователя
Введите цифру [ 2 ] если хотите совершить вход в профиль
Введите цифру [ 3 ] если хотите сбросить пароль для входа
Для выхода введите любой символ кроме 1, 2, 3"""


"""Создаём базу данных registration.db"""
db = sqlite3.connect("registration.db") # Создаем БД и подключаемся к ней
cur = db.cursor() # Переменная для управления базы данных
print("1. Создали и подключились к базе данных registration.db")
db.commit() # Сохраняем все изменения

"""Создаём таблицу users_data, если она не создана.
Задаем названия и тип данных для колонок."""
cur.execute("""
    CREATE TABLE IF NOT EXISTS users_data(
        UserID INTEGER PRIMARY KEY AUTOINCREMENT,
        Login TEXT NOT NULL UNIQUE,
        Password TEXT NOT NULL,
        Code INTEGER NOT NULL);
""")
print("2. Создали таблицу users_data и задали типы данных для колонок")
db.commit() # Сохраняем все изменения

"""Вносим первого пользователя в таблицу.
Безопасным способом от SQL-инъекций.
Игнорируем вставку, если он уже есть."""
insert_params = ('Ivan', 'qwer1234', 1234)
cur.execute(
    """INSERT OR IGNORE INTO users_data (Login, Password, Code)
            VALUES (?, ?, ?);""", insert_params) # OR IGNORE чтобы не было ошибки о том что Ivan уже есть

print("3. Добавили первого пользователя в таблицу")
db.commit() # Сохраняем все изменения

def check_user(login, password, sicret_code):
    """Проверка введенных данных пользователем"""

    if len(login) < 3:
        raise Exception ('\033[31mОшибка ввода\033[0m: Логин должен быть не меньше 3 символов')
    if len(password) < 3:
        raise Exception ('\033[31mОшибка ввода\033[0m: Пароль должен быть не меньше 3 символов')
    if sicret_code.isdigit() is not True and len(sicret_code) != 4:
        raise Exception ('\033[31mОшибка ввода\033[0m: Секретный код должен быть только из 4 цифр')

def check_user_in_base(login, password):
    """Проверка логина и пароля в базе данных"""

    search_user = login
    cur.execute(f"""SELECT * FROM users_data WHERE Login = ?;""", (search_user,)) # Безопасное прочтение БД
    user = cur.fetchone()

    if user is None:
        raise Exception(f'\033[31mОшибка\033[0m: {login} нет в базе. Введите логин зарегистрированного пользователя')
    if user[1] == login and user[2] != password:
        raise Exception(f'\033[31mОшибка\033[0m: Для пользователя {login} введен неверный пароль. Повторите попытку')

def check_user_and_sicret_code(login, sicret_code):
    """Проверяем логин пользователя и его секретный код"""

    search_user = login
    cur.execute(f"""SELECT * FROM users_data WHERE Login = ?;""", (search_user,))  # Безопасное прочтение БД по логину
    user = cur.fetchone()

    if user is None :
        raise Exception(f'\033[31mОшибка\033[0m: {login} нет в базе. Введите логин зарегистрированного пользователя')
    if user[1] == login and str(user[3]) != sicret_code:
        raise Exception (f'\033[31mОшибка\033[0m: Для пользователя {login} введен неверный секретный код. Повторите попытку')

    else:
        print(f"Совершен вход для пользователя {login}\nВведите новый пароль:")
        new_password = input()
        if len(new_password) < 3:
            raise Exception('\033[31mОшибка ввода\033[0m: Пароль должен быть не меньше 3 символов')

        else:
            params = (new_password, login,)
            cur.execute("""UPDATE users_data SET Password = ? WHERE Login = ?""", params)


def reg_new_user():
    """Регистрируем нового пользователя"""

    while True:
        try:
            print("Введите логин: ")
            login = input()
            print("Введите пароль: ")
            password = input()
            print("Введите секретный код из цифр: ")
            sicret_code = input()

            check_user(login, password, sicret_code) # Вызываем функцию проверки логина, пароля и секретного кода

            insert_user = (login, password, sicret_code)
            cur.execute(
                """INSERT INTO users_data (Login, Password, Code)
                        VALUES (?, ?, ?);""", insert_user)
            db.commit()
            print('Новый пользователь успешно зарегистрирован')
            print(txt_choice)
            break

        except sqlite3.IntegrityError:
            # Ошибка UNIQUE (логин уже существует)
            print('\033[31mОшибка:\033[0m Пользователь с таким логином уже существует!')

        except Exception as e:
            print(e)

def log_in():
    """Авторизация в системе"""

    while True:
        try:
            print("Введите логин:")
            login = input()
            print("Введите пароль:")
            password = input()

            check_user_in_base(login, password) # Вызываем функцию для проверки пользователя в базе

            print(f"Пользователь {login} успешно совершил вход в систему")
            print("\033[31mТут просто как вход в систему оставил - конец кода.\033[0m")
            print()
            print(txt_choice)
            break
        except Exception as e:
            print(e)

def drop_password():
    """Функция сброса пароля для пользователя"""

    while True:
        try:
            print("Введите логин:")
            login = input()
            print("Введите секретный код:")
            sicret_code = input()

            check_user_and_sicret_code(login, sicret_code) # Вызываем функцию для проверки логина и секретного кода
            db.commit()  # Сохраняем все изменения

            print(f"Для пользователя {login} сброшен старый пароль.\n")
            print(txt_choice)
            break

        except Exception as e:
            print(e)

print("Добро пожаловать на сайт www.slezaprogrammista.ru\n"
      "Введите цифру [ 1 ] если хотите зарегистрировать нового пользователя\n"
      "Введите цифру [ 2 ] если хотите совершить вход в профиль\n"
      "Введите цифру [ 3 ] если хотите сбросить пароль для входа\n"
      "Для выхода введите любой символ кроме 1, 2, 3")

while True:
    match input():
        case '1':
            reg_new_user()
        case '2':
            log_in()
        case '3':
            drop_password()
        case _:
            exit()
