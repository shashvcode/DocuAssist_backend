from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models import db, User

auth = Blueprint("auth", __name__)

@auth.route("/signup", methods = ["POST"])
def signup():
    data = request.get_json()

    if "name" not in data or "email" not in data or "password" not in data:
        return jsonify({"error": "name, email, and password are required"}), 400

    existing_user = User.query.filter_by(email=data["email"]).first()
    if existing_user:
        return jsonify({"error": "User already exists"}), 400
    
    user = User(name=data["name"], email=data["email"])
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!"}), 201

@auth.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    user = User.query.filter_by(email=data["email"]).first()
    if user and user.check_password(data["password"]):
        token = create_access_token(identity=str(user.id))
        return jsonify({"token": token}), 200

    return jsonify({"error": "Invalid credentials"}), 401