import re
#pip install flask
from flask import Flask, render_template, request, redirect, url_for, jsonify
from db import create_table, add_user, authenticate_user
from search import load_papers, search_papers  # Import functions

# Load papers data on application startup (assuming 'all_papers.csv' is in the same directory)
papers = load_papers('all_papers.csv')  # Modify path if needed


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


# @app.route('/home', methods=['GET', 'POST'])
# def home():
#     if request.method == 'POST':
#         keyword = request.form['keyword']
#         matching_papers = search_papers(keyword, papers)
#         return render_template('home.html', papers=matching_papers, keyword=keyword)
#     return render_template('home.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/search', methods=['POST'])
def search():
    keyword = request.json['keyword'].lower()  # Get search keyword
    matching_papers = search_papers(keyword, papers)
    return jsonify(matching_papers)

# @app.route('/search')
# def search():
#     if request.method == 'POST':
#         keyword = request.form['keyword']
#         search_results = search_papers(keyword, papers)  # Search using loaded data
#     else:
#         keyword = ""
#         search_results = None

#     return render_template('home.html', keyword=keyword, search_results=search_results)


@app.route('/view')
def view():
    return render_template('view.html')

@app.route('/page1')
def page():
    return render_template('page1.html')





if __name__ == '__main__':
    app.run(debug=True)





