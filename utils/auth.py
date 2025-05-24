import json
import os
import hashlib

USER_FILE = "users.json"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

def register_user(username, email, password, confirm_password):
    if password != confirm_password:
        return False, "Password dan konfirmasi password tidak cocok."
    
    users = load_users()
    if email in users:
        return False, "Email sudah digunakan."
    
    users[email] = {
        "username": username,
        "password": hash_password(password)
    }
    save_users(users)
    return True, "Registrasi berhasil!"

def login_user(email, password):
    users = load_users()
    if email in users and users[email]["password"] == hash_password(password):
        return True
    return False

def update_username(email, new_username):
    users = load_users()
    if email in users:
        users[email]["username"] = new_username
        save_users(users)
        return True
    return False
