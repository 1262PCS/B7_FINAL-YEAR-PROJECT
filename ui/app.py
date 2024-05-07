import re
from flask import Flask, jsonify, render_template, request, redirect, url_for
from db import create_table, add_user, authenticate_user
from search import search_papers,display_results


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
            return redirect(url_for('search'))
        
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



@app.route('/search',methods=['GET','POST'])
def search():
    if request.method == "POST":
        userInput = request.form.get('search')
        print('Received userInput:', userInput) 
        search_result=search_papers(userInput)
        results= display_results(search_result)
        return render_template('search.html', result=results)
        # print(results)
        # # return results
        # return jsonify({'result': results})
        # # render_template('search_result.html',result=results)
    return render_template('search.html')




@app.route('/view')
def view():
    return render_template('view.html')

@app.route('/page1')
def page():
    return render_template('page1.html')

@app.route('/result')
def result():
    return render_template('result.html')





if __name__ == '__main__':
    app.run(debug=True)





