from flask import Flask, render_template, request, redirect, url_for, session
import json, os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'tmoonsecret'

def load_users():
    if os.path.exists('users.json'):
        with open('users.json') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        users = load_users()
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return "User already exists."
        users[username] = {
            'password': generate_password_hash(password),
            'coins': 0
        }
        save_users(users)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = load_users()
        username = request.form['username']
        password = request.form['password']
        if username in users and check_password_hash(users[username]['password'], password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        return "Invalid credentials."
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    users = load_users()
    username = session['username']
    coins = users[username]['coins']
    return render_template('dashboard.html', username=username, coins=coins)

@app.route('/recharge', methods=['GET', 'POST'])
def recharge():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        amount = int(request.form['amount'])
        users = load_users()
        username = session['username']
        users[username]['coins'] += amount
        save_users(users)
        return redirect(url_for('dashboard'))
    return render_template('recharge.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
