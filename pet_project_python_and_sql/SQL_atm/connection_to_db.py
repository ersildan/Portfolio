import sqlite3 as s

db = s.connect('SQL_atm/atm.db')
cur = db.cursor()
cur.execute("select * from Users_data")
result = cur.fetchall()

print(result)
