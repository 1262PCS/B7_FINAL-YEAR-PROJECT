from flask import Flask, render_template, request, redirect, url_for
from function import validate_user
from db import create_table, add_user, authenticate_user

app = Flask(__name__)

# Dummy database for users (replace this with a real database in production)
create_table()

@app.route('/')
def first():
    return render_template('page1.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Check if username and password match in the database
        if authenticate_user(username, password): 
                # Redirect to home page upon successful login
            return redirect(url_for('home'))
        # If credentials don't match, show login page again
        return render_template('login.html', message='Invalid username or password')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Check if username already exists
        if not authenticate_user(username, password):
            # If username is unique, add the user to the database
            add_user(username, password)
            # Redirect to login page after successful signup
            return redirect(url_for('login'))
        return render_template('signup.html', message='Username already exists')
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)
