import sqlite3
from hashlib import sha256

# Function to create the database table
def create_table():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                 username TEXT UNIQUE NOT NULL, 
                 password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Function to add a new user to the database
def add_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    hashed_password = sha256(password.encode()).hexdigest()  # Hash the password before storing
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
    conn.commit()
    conn.close()

# Function to authenticate a user
def authenticate_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    hashed_password = sha256(password.encode()).hexdigest()  # Hash the password for comparison
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed_password))
    user = c.fetchone()
    conn.close()
    return user is not None

# Create the database table if it doesn't exist
# create_table()

# # Example usage:
# # Add a new user
# add_user('user1', 'password123')

# # Authenticate a user
# authenticated = authenticate_user('user1', 'password123')
# print("User authenticated:", authenticated)
