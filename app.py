from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, auth

app = Flask(__name__)

# Initialize Firebase
cred = credentials.Certificate("path/to/serviceAccountKey.json")
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
    except:
        return jsonify({"error": "Invalid credentials"}), 401

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
    except:
        return jsonify({"error": "User creation failed"}), 400

if __name__ == '__main__':
    app.run(debug=True)