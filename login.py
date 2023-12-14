from flask import Flask, render_template, request, redirect, url_for, flash
import re

app = Flask(__name__)
app.secret_key = 'jkps'  # Change this to a secure secret key

# For simplicity, using a list as a user database. In a real application, use a database.
users = [
    {'username': 'Janvi', 'password': 'janvi', 'email': 'janviajith@gmail.com'},
    {'username': 'Poonam', 'password': 'poonam', 'email': 'poonamcsanil@gmail.com'},
    {'username': 'Kavya', 'password': 'kavya', 'email': 'krishkavya@gmail.com'},
    {'username': 'Sthuthi', 'password': 'sthuthi', 'email': 'sthuthi@gmail.com'}
]

# Route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['psw']
        

        # Check if the provided username and password match a user in the database
        user = next((user for user in users if user['username'] == username and user['password'] == password), None)

        if user:
            # If the user is found, set a session variable and redirect to a secure page
            # In a real application, use a more secure method for session management
            flash('Login successful', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('log.html')

def is_valid_email(email):
    # Basic email validation using a regular expression
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

# Route for the sign-up page
@app.route('/sign')
def sign():
    if request.method == 'POST':
        user = request.form['uname']
        email = request.form['email']
        pswd = request.form['psw']
        
        # Check email validity
        if not is_valid_email(email):
            flash('Invalid email format', 'error')
            return render_template('sign.html')
        
        return redirect(url_for('login'))

    return render_template('sign.html')

# Route for the index page
@app.route('/index')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
