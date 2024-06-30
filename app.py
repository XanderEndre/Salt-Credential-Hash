import json
import sqlite3
import hashlib
import re
from flask import Flask, jsonify, request, g

app = Flask(__name__)

# Database File Name
DATABASE = 'database.db'

# Utility function to get database connection
def get_db():
    if not hasattr(g, '_database'):
        g._database = sqlite3.connect(DATABASE)
    return g._database

# Utility function to create the users table if it does not exist
def create_table():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    db.commit()

# Utility function to hash passwords using SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Utility function to validate password
def validate_password(password):
    return re.search(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", password)

# Utility function to check if a user exists
def user_exists(username):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    return cursor.fetchone()

# Utility function to authenticate user
def authenticate_user(username, password):
    db = get_db()
    cursor = db.cursor()
    hashed_password = hash_password(password)
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
    return cursor.fetchone()

# Initialize the database table
with app.app_context():
    create_table()

# Route to register the user
@app.route('/register', methods=['POST'])
def create_user():
    if request.content_type != 'application/json':
        return jsonify({"error": "Unsupported Media Type: Content-Type must be 'application/json'"}), 415

    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"error": "Missing username or password"}), 400

        if not validate_password(password):
            return jsonify({"error": "Password must be at least 8 characters long and include at least 1 number"}), 400

        if user_exists(username):
            return jsonify({"error": "Username already exists"}), 400

        db = get_db()
        cursor = db.cursor()
        hashed_password = hash_password(password)
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        db.commit()

        return jsonify({"message": "User created successfully"}), 201
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

# Route to login the user
@app.route('/login', methods=['POST'])
def login_user():
    if request.content_type != 'application/json':
        return jsonify({"error": "Unsupported Media Type: Content-Type must be 'application/json'"}), 415

    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"error": "Missing username or password"}), 400

        if not authenticate_user(username, password):
            return jsonify({"error": "Invalid login. Incorrect username or password."}), 400

        return jsonify({"message": "Login successful"}), 200
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

# Route to update the user
@app.route('/update', methods=['PATCH'])
def update_user():
    if request.content_type != 'application/json':
        return jsonify({"error": "Unsupported Media Type: Content-Type must be 'application/json'"}), 415
    
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        new_password = data.get("new_password")

        if not username or not password or not new_password:
            return jsonify({"error": "Missing username, password, or new_password"}), 400
        
        if not validate_password(new_password):
            return jsonify({"error": "New password must be at least 8 characters long and include at least 1 number"}), 400

        if not authenticate_user(username, password):
            return jsonify({"error": "Invalid login. Incorrect username or password."}), 400
        
        db = get_db()
        cursor = db.cursor()
        new_hashed_password = hash_password(new_password)
        cursor.execute("UPDATE users SET password = ? WHERE username = ?", (new_hashed_password, username))
        db.commit()
        
        return jsonify({"message": "Password updated successfully"}), 200
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
