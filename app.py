from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

def get_db():
    return sqlite3.connect("database.db")

@app.route('/')
def home():
    db = get_db()
    products = db.execute("SELECT * FROM products").fetchall()
    return render_template("index.html", products=products)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']
        db = get_db()
        data = db.execute("SELECT * FROM users WHERE username=? AND password=?", (user,pwd)).fetchone()
        if data:
            session['user'] = user
            return redirect('/admin')
    return render_template("login.html")

@app.route('/admin')
def admin():
    if 'user' not in session:
        return redirect('/login')
    return render_template("admin.html")

@app.route('/add_product', methods=['POST'])
def add_product():
    name = request.form['name']
    price = request.form['price']
    stock = request.form['stock']
    db = get_db()
    db.execute("INSERT INTO products (name, price, stock) VALUES (?,?,?)",(name,price,stock))
    db.commit()
    return redirect('/admin')

@app.route('/sale', methods=['POST'])
def sale():
    product_id = request.form['product_id']
    qty = int(request.form['qty'])
    db = get_db()
    product = db.execute("SELECT stock, price FROM products WHERE id=?",(product_id,)).fetchone()
    new_stock = product[0] - qty
    total = product[1] * qty
    db.execute("UPDATE products SET stock=? WHERE id=?",(new_stock,product_id))
    db.execute("INSERT INTO sales (product_id, qty, total) VALUES (?,?,?)",(product_id,qty,total))
    db.commit()
    return "Sale Done. Total: " + str(total)

app.run(host='0.0.0.0', port=81)
