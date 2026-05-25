#!/usr/bin/env python3
"""
Vulnerable Web Application - CodeAlpha Internship
DO NOT USE IN PRODUCTION
"""

from flask import Flask, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'hardcoded_secret_key_12345'

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT, password TEXT, email TEXT)''')
    c.execute("INSERT OR IGNORE INTO users VALUES (1, 'admin', 'admin123', 'admin@example.com')")
    c.execute("INSERT OR IGNORE INTO users VALUES (2, 'user1', 'password123', 'user1@example.com')")
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return '<h1>Welcome to SecureBank</h1><a href="/login">Login</a> | <a href="/register">Register</a> | <a href="/search">Search Users</a>'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # VULNERABLE: SQL Injection
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        c.execute(query)
        user = c.fetchone()
        conn.close()
        
        if user:
            session['user'] = username
            return f"<h2>Welcome {username}!</h2><a href='/profile'>View Profile</a>"
        else:
            return "<h2>Login failed!</h2>"
    
    return '<form method="POST">Username: <input type="text" name="username"><br>Password: <input type="password" name="password"><br><input type="submit" value="Login"></form>'

@app.route('/profile')
def profile():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    user = session['user']
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute(f"SELECT * FROM users WHERE username='{user}'")
    user_data = c.fetchone()
    conn.close()
    
    # VULNERABLE: XSS
    msg = request.args.get('msg', 'Hello!')
    return f'<h2>Profile</h2><p>Username: {user_data[1]}</p><p>Email: {user_data[3]}</p><p>Welcome message: {msg}</p>'

@app.route('/search')
def search():
    # VULNERABLE: SQL Injection
    query = request.args.get('q', '')
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute(f"SELECT * FROM users WHERE username LIKE '%{query}%'")
    results = c.fetchall()
    conn.close()
    
    output = "<h2>Search Results</h2>"
    for user in results:
        output += f"<p>{user[1]} - {user[3]}</p>"
    return output

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        # VULNERABLE: Plaintext passwords
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute(f"INSERT INTO users (username, password, email) VALUES ('{username}', '{password}', '{email}')")
        conn.commit()
        conn.close()
        
        return f"<h2>User {username} registered!</h2>"
    
    return '<form method="POST">Username: <input type="text" name="username"><br>Password: <input type="password" name="password"><br>Email: <input type="text" name="email"><br><input type="submit" value="Register"></form>'

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
