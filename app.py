from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, auth
import os
import json

app = Flask(__name__)

# Load Firebase credentials from environment variable
firebase_credentials = os.getenv('FIREBASE_CREDENTIALS')
if not firebase_credentials:
    raise ValueError("No Firebase credentials found in environment variables.")

# Parse the JSON string
cred_dict = json.loads(firebase_credentials)

# Initialize Firebase
cred = credentials.Certificate(cred_dict)
firebase_admin.initialize_app(cred)

# Login API
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # Authenticate user using Firebase
    try:
        user = auth.get_user_by_email(email)
        return jsonify({"message": "Login successful", "user_id": user.uid}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401

# Signup API
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # Create user using Firebase
    try:
        user = auth.create_user(email=email, password=password)
        return jsonify({"message": "User created", "user_id": user.uid}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
