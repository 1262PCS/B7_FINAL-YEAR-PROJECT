import re
from flask import Flask, render_template, request, redirect, url_for
from db import create_table, add_user, authenticate_user


app = Flask(__name__)

create_table()

@app.route('/')
def first():
    return render_template('page1.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['psw']
        
        if authenticate_user(email, password): 
            return redirect(url_for('home'))
        
        return render_template('login.html', message='Invalid username or password')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['uname']
        email = request.form['email']
        password = request.form['psw']
        confirm_password = request.form['confirm']

        if password != confirm_password:
            return render_template('signup.html', message='Passwords do not match')

        try:
            add_user(username, email, password)
            return redirect(url_for('login'))
        except ValueError as e:
            return render_template('signup.html', message=str(e))

    return render_template('signup.html')


@app.route('/home')
def home():
    return render_template('home.html')



if __name__ == '__main__':
    app.run(debug=True)
