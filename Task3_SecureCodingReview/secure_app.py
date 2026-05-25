#!/usr/bin/env python3
"""
Secure Web Application - CodeAlpha Internship
Fixed version of vulnerable_app.py
"""

from flask import Flask, request, redirect, url_for, session
from markupsafe import escape
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'fallback-dev-key-only')

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT, password TEXT, email TEXT)''')
    
    hashed_admin = generate_password_hash('admin123')
    hashed_user = generate_password_hash('password123')
    c.execute("INSERT OR IGNORE INTO users VALUES (1, 'admin', ?, 'admin@example.com')", (hashed_admin,))
    c.execute("INSERT OR IGNORE INTO users VALUES (2, 'user1', ?, 'user1@example.com')", (hashed_user,))
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return '<h1>Welcome to SecureBank (SECURE)</h1><a href="/login">Login</a> | <a href="/register">Register</a> | <a href="/search">Search Users</a>'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        user = c.fetchone()
        conn.close()
        
        if user and check_password_hash(user[2], password):
            session['user'] = username
            return f"<h2>Welcome {escape(username)}!</h2><a href='/profile'>View Profile</a>"
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
    c.execute("SELECT * FROM users WHERE username=?", (user,))
    user_data = c.fetchone()
    conn.close()
    
    msg = escape(request.args.get('msg', 'Hello!'))
    return f'<h2>Profile</h2><p>Username: {escape(user_data[1])}</p><p>Email: {escape(user_data[3])}</p><p>Welcome message: {msg}</p>'

@app.route('/search')
def search():
    query = request.args.get('q', '')
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username LIKE ?", (f'%{query}%',))
    results = c.fetchall()
    conn.close()
    
    output = "<h2>Search Results</h2>"
    for user in results:
        output += f"<p>{escape(user[1])} - {escape(user[3])}</p>"
    return output

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        hashed_password = generate_password_hash(password)
        
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", 
                  (username, hashed_password, email))
        conn.commit()
        conn.close()
        
        return f"<h2>User {escape(username)} registered!</h2>"
    
    return '<form method="POST">Username: <input type="text" name="username"><br>Password: <input type="password" name="password"><br>Email: <input type="text" name="email"><br><input type="submit" value="Register"></form>'

if __name__ == '__main__':
    init_db()
    app.run(debug=False, host='0.0.0.0', port=5000)
