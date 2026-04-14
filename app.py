import os
import psycopg2
from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'smart_canteen_secret_key'

# --- DATABASE CONNECTION ---
def get_db_connection():
    # This pulls the 'POSTGRES_URL' you set in Vercel Settings
    conn = psycopg2.connect(os.environ.get('POSTGRES_URL'), sslmode='require')
    return conn

# --- INITIALIZE DATABASE (Creates tables and adds your menu) ---
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Create Users Table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY, 
            username TEXT UNIQUE, 
            password TEXT, 
            role TEXT
        )
    ''')
    
    # Create Menu Table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS menu (
            id SERIAL PRIMARY KEY, 
            category TEXT, 
            name TEXT, 
            price REAL, 
            description TEXT, 
            emoji TEXT
        )
    ''')
    
    # Create Orders Table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id SERIAL PRIMARY KEY, 
            username TEXT, 
            items TEXT, 
            total REAL, 
            status TEXT, 
            timestamp TEXT
        )
    ''')

    # Insert your specific menu items if table is empty
    cur.execute('SELECT COUNT(*) FROM menu')
    if cur.fetchone()[0] == 0:
        menu_items = [
            ('Snacks', 'Crispy French Fries', 60, 'Salted potato fries served with ketchup', '🍟'),
            ('Snacks', 'Punjabi Samosa (2pcs)', 40, 'Hot samosas with mint and tamarind chutney', '🥟'),
            ('Fast Food', 'Margherita Pizza', 120, 'Classic cheese pizza with a thin crust', '🍕'),
            ('Fast Food', 'Aloo Tikki Burger', 70, 'Crispy patty with fresh veggies and mayo', '🍔'),
            ('Fast Food', 'White Sauce Pasta', 140, 'Creamy penne pasta with sweet corn and herbs', '🍝'),
            ('Meals', 'Rajma Chawal Bowl', 90, 'Authentic homestyle rajma with basmati rice', '🍛'),
            ('Meals', 'Chole Bhature (2pcs)', 100, 'Spicy punjabi chole with fluffy bhature', '🍲'),
            ('Beverages', 'Cold Coffee', 80, 'Thick blended coffee with chocolate syrup', '🧋'),
            ('Beverages', 'Fresh Lime Soda', 50, 'Refreshing sweet and salted lime drink', '🍹')
        ]
        for item in menu_items:
            cur.execute('INSERT INTO menu (category, name, price, description, emoji) VALUES (%s, %s, %s, %s, %s)', item)

    # Insert default users if empty
    cur.execute('SELECT COUNT(*) FROM users')
    if cur.fetchone()[0] == 0:
        cur.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", ('admin', 'admin', 'admin'))
        cur.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", ('student', 'pass', 'student'))

    conn.commit()
    cur.close()
    conn.close()

# Run initialization
try:
    init_db()
except Exception as e:
    print(f"Database Init Error: {e}")

# --- ROUTES ---

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user:
        session['username'] = user[1]
        session['role'] = user[3]
        if user[3] == 'admin':
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('menu'))
    
    flash('Invalid Credentials!')
    return redirect(url_for('index'))

@app.route('/menu')
def menu():
    if 'username' not in session: return redirect(url_for('index'))
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM menu')
    items = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('menu.html', items=items)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    item_name = request.form.get('item_name')
    item_price = float(request.form.get('item_price'))
    
    if 'cart' not in session: session['cart'] = []
    cart = session['cart']
    cart.append({'name': item_name, 'price': item_price})
    session['cart'] = cart
    return redirect(url_for('menu'))

@app.route('/cart')
def view_cart():
    cart = session.get('cart', [])
    total = sum(item['price'] for item in cart)
    return render_template('cart.html', cart=cart, total=total)

@app.route('/checkout', methods=['POST'])
def checkout():
    cart = session.get('cart', [])
    if not cart: return redirect(url_for('menu'))
    
    total = sum(item['price'] for item in cart)
    items_str = ", ".join([item['name'] for item in cart])
    timestamp = datetime.now().strftime("%I:%M %p | %d %b")
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO orders (username, items, total, status, timestamp) VALUES (%s, %s, %s, %s, %s)',
                (session['username'], items_str, total, 'Pending', timestamp))
    conn.commit()
    cur.close()
    conn.close()
    
    session.pop('cart', None)
    return redirect(url_for('orders'))

@app.route('/orders')
def orders():
    if 'username' not in session: return redirect(url_for('index'))
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM orders WHERE username = %s ORDER BY id DESC', (session['username'],))
    user_orders = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('orders.html', orders=user_orders)

@app.route('/admin')
def admin_dashboard():
    if session.get('role') != 'admin': return redirect(url_for('index'))
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM orders ORDER BY id DESC')
    all_orders = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('admin.html', orders=all_orders)

@app.route('/update_status/<int:order_id>/<status>')
def update_status(order_id, status):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE orders SET status = %s WHERE id = %s', (status, order_id))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('admin_dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run()
