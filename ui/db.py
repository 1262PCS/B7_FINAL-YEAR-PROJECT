import sqlite3
from hashlib import sha256

from email_validator import EmailNotValidError, validate_email


def create_table():

    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                 email TEXT NOT NULL,
                 username TEXT UNIQUE NOT NULL, 
                 password TEXT NOT NULL)''')
    
    conn.commit()
    conn.close()


def add_user(username, email, password):

    try:
        validate_email(email)
    except EmailNotValidError:
        raise ValueError("Invalid email address")

    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE email=?", (email,))

    existing_user = c.fetchone()

    if existing_user:
        conn.close()
        raise ValueError("Email already exists")

    
    hashed_password = sha256(password.encode()).hexdigest()


    c.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, hashed_password, email))
    
    conn.commit()
    conn.close()


def authenticate_user(email, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    hashed_password = sha256(password.encode()).hexdigest() 

    c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, hashed_password))

    user = c.fetchone()
    conn.close()

    return user is not None


# create_table()

# add_user('user1', 'password123')

# authenticated = authenticate_user('user1', 'password123')
# print("User authenticated:", authenticated)
