import sqlite3

conn=sqlite3.connect('todo.sqlite')
cursor = conn.cursor()
cursor.execute("SELECT * FROM items")
rows = cursor.fetchall()

for row in rows:
    print(row)