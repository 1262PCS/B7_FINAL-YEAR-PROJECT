import re
from flask import Flask, jsonify, render_template, request, redirect, url_for
from db import create_table, add_user, authenticate_user
from search import search_papers,display_results
from view import paper_data_title,paper_data_author,paper_data_citations,paper_data_publisher, paper_pdf_link,view_abstract,paper_community

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
    return render_template('search.html')



@app.route('/view', methods=['GET'])
def view():
    item_content = request.args.get('item')
    title = paper_data_title(item_content)
    authors=paper_data_author(item_content)
    citations = paper_data_citations(item_content)
    Publisher = paper_data_publisher(item_content)
    link = paper_pdf_link(item_content)
    abstract = view_abstract(item_content)
    community = paper_community(item_content)
    return render_template('view.html',result = title, authors =authors,citations =citations, Publisher=Publisher, link = link,abstract = abstract, community = community)

@app.route('/page1')
def page():
    return render_template('page1.html')

@app.route('/result')
def result():
    return render_template('result.html')





if __name__ == '__main__':
    app.run(debug=True)





