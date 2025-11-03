import sqlite3 as s


# чекаем подключение к бд

db = s.connect('atm.db')
cur = db.cursor()
cur.execute("select * from Users_data")
result = cur.fetchall()

print(result)
