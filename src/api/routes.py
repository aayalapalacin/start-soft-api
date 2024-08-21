"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
import datetime


api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    expiration = datetime.timedelta(days=3)
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify("Email/Password are incorrect"),401
    if not check_password_hash(user.password,password):
        return jsonify("Email/Password are incorrect"),401
    
    access_token = create_access_token(identity=email,expires_delta=expiration)
    return jsonify(access_token=access_token),200
    
@api.route("/signup", methods=["POST"])
def signup():
    name = request.json.get("name", None)
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    phone = request.json.get("phone", None)
    role = request.json.get("role", None)
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({"msg": "user already exist"}), 401
    new_user = User(
        name=name,
        email=email,
        password= generate_password_hash(password),
        phone=phone,
        role=role,
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify("user created successfully")

@api.route("/users", methods=["GET"])
def get_users():
    users_list = User.query.all() 
    users_serialized = [user.serialize() for user in users_list] 
    return jsonify(users_serialized), 200



@api.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify("user does not exists")
    else:
        return jsonify(user.serialize()), 200


@api.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.json
    user.name = data.get("name", user.name)
    user.email = data.get("email", user.email)
    if data.get("password"):
        user.password = generate_password_hash(data.get("password"))
    user.phone = data.get("phone", user.phone)
    user.role = UserRole[data.get("role").upper()] if data.get("role") else user.role
    db.session.commit()
    return jsonify(user.serialize()), 200

# Delete a user by ID
@api.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"msg": "User deleted successfully"}), 200