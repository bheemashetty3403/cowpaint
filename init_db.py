import sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT, price REAL, stock INTEGER)")
c.execute("CREATE TABLE IF NOT EXISTS sales (id INTEGER PRIMARY KEY, product_id INTEGER, qty INTEGER, total REAL)")

# default admin
c.execute("INSERT INTO users (username,password) VALUES ('admin','admin')")

conn.commit()
conn.close()
