import re
from flask import Flask, render_template, request, redirect, url_for
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
        email = request.form['email']
        password = request.form['psw']
        # Check if username and password match in the database
        if authenticate_user(email, password): 
                # Redirect to home page upon successful login
            return redirect(url_for('home'))
        # If credentials don't match, show login page again
        return render_template('login.html', message='Invalid username or password')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['uname']
        email = request.form['email']
        password = request.form['psw']
        confirm_password = request.form['confirm']

        # Check if passwords match
        if password != confirm_password:
            return render_template('signup.html', message='Passwords do not match')

        try:
            # Attempt to add the user to the database
            add_user(username, email, password)
            # Redirect to login page after successful signup
            return redirect(url_for('login'))
        except ValueError as e:
            # Handle the ValueError raised by add_user
            return render_template('signup.html', message=str(e))

    return render_template('signup.html')


@app.route('/home')
def home():
    return render_template('home.html')



if __name__ == '__main__':
    app.run(debug=True)
