
def validate_user(username, password, users):
    for user in users:
        if user['username'] == username and user['password'] == password:
            return True
    return False