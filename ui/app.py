from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dummy database for users (replace this with a real database in production)
users = []

@app.route('/')
def first():
    return render_template('page1.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Check if username and password match in the database
        for user in users:
            if user['username'] == username and user['password'] == password:
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
        for user in users:
            if user['username'] == username:
                return render_template('signup.html', message='Username already exists')
        # If username is unique, add the user to the database
        users.append({'username': username, 'password': password})
        # Redirect to login page after successful signup
        return redirect(url_for('login'))
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)
