from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('hotel_data.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS hotel_info (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        hotel_name TEXT,
        address TEXT,
        email TEXT,
        phone TEXT,
        language TEXT
    )""")
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['hotel_name']
    address = request.form['address']
    email = request.form['email']
    phone = request.form['phone']
    language = request.form['language']
    
    conn = sqlite3.connect('hotel_data.db')
    c = conn.cursor()
    c.execute("INSERT INTO hotel_info (hotel_name, address, email, phone, language) VALUES (?, ?, ?, ?, ?)",
              (name, address, email, phone, language))
    conn.commit()
    conn.close()
    
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    conn = sqlite3.connect('hotel_data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM hotel_info")
    data = c.fetchall()
    conn.close()
    return render_template('dashboard.html', hotels=data)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
