"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Project, Task, Contract, Choice
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
        return jsonify({"msg": "Email/Password are incorrect"}),401
    if not check_password_hash(user.password,password):
        return jsonify({"msg": "Email/Password are incorrect"}),401
    
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
    
    return jsonify({"msg":"user created successfully","result": new_user.serialize()})

@api.route("/users", methods=["GET"])
def get_users():
    users_list = User.query.all() 
    users_serialized = [user.serialize() for user in users_list] 
    return jsonify(users_serialized), 200



@api.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"msg": "user does not exists"})
    else:
        return jsonify(user.serialize()), 200


@api.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    data = request.json
    user.name = data.get("name", user.name)
    user.email = data.get("email", user.email)
    user.phone = data.get("phone", user.phone)
    user.role = data.get("role", user.role)
    db.session.commit()
    return jsonify({"msg":"user updated!","result":user.serialize()}), 200


@api.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    return jsonify({"msg": "User deleted successfully"}), 200



# projects
@api.route("/projects", methods=["POST"])
def create_project():
    data = request.json
    new_project = Project(
        name=data.get("name"),
        description=data.get("description"),
        client_id=data.get("client_id"),
        status=data.get("status"),
        is_completed=data.get("is_completed"),
    )
    db.session.add(new_project)
    db.session.commit()
    return jsonify({"msg":"project created", "result": new_project.serialize()}), 201


@api.route("/projects", methods=["GET"])
def get_projects():
    projects_list = Project.query.all()
    projects_serialized = [project.serialize() for project in projects_list]
    return jsonify(projects_serialized), 200


@api.route("/projects/<int:project_id>", methods=["GET"])
def get_project(project_id):
    project = Project.query.filter_by(id=project_id).first()
    if not project:
        return jsonify({"msg":"Project does not exist"}), 404
    return jsonify(project.serialize()), 200


@api.route("/projects/<int:project_id>", methods=["PUT"])
def update_project(project_id):
    project = Project.query.filter_by(id=project_id).first()
    if not project:
        return jsonify({"msg":"Project does not exist"}), 404
    data = request.json
    project.name = data.get("name", project.name)
    project.description = data.get("description", project.description)
    project.status = data.get("status", project.status)
    project.is_completed = data.get("is_completed", project.is_completed)
    db.session.commit()
    return jsonify({"msg": "project updated","result":project.serialize()}), 200

# Delete a project by ID
@api.route("/projects/<int:project_id>", methods=["DELETE"])
def delete_project(project_id):
    project = Project.query.filter_by(id=project_id).first()
    if not project:
        return jsonify({"msg":"Project does not exist"}), 404
    db.session.delete(project)
    db.session.commit()
    return jsonify({"msg": "Project deleted successfully"}), 200



# tasks

@api.route("/tasks", methods=["POST"])
def create_task():
    data = request.json
    new_task = Task(
        name=data.get("name"),
        description=data.get("description"),
        project_id=data.get("project_id"),
        contractor_id=data.get("contractor_id"),
        status=data.get("status"),
        is_completed=data.get("is_completed", False),
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"msg":"task created","result":new_task.serialize()}), 201

# Get all tasks
@api.route("/tasks", methods=["GET"])
def get_tasks():
    tasks_list = Task.query.all()
    tasks_serialized = [task.serialize() for task in tasks_list]
    return jsonify(tasks_serialized), 200

# Get a task by ID
@api.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if not task:
        return jsonify({"msg":"Task does not exist"}), 404
    return jsonify(task.serialize()), 200

# Update a task by ID
@api.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if not task:
        return jsonify({"msg":"Task does not exist"}), 404
    data = request.json
    task.name = data.get("name", task.name)
    task.description = data.get("description", task.description)
    task.status = data.get("status", task.status)
    task.is_completed = data.get("is_completed", task.is_completed)
    db.session.commit()
    
    return jsonify({"msg":"task updated","result":task.serialize()}), 200

# Delete a task by ID
@api.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if not task:
        return jsonify({"msg":"Task does not exist"}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({"msg": "Task deleted successfully"}), 200

# contract

# Create a new contract
@api.route("/contracts", methods=["POST"])
def create_contract():
    data = request.json
    new_contract = Contract(
        project_id=data.get("project_id"),
        contractor_id=data.get("contractor_id"),
        terms=data.get("terms"),
        client_signature=data.get("client_signature", False),
        contractor_signature=data.get("contractor_signature", False),
    )
    db.session.add(new_contract)
    db.session.commit()
    return jsonify({"msg":"contract created","result":new_contract.serialize()}), 201

# Get all contracts
@api.route("/contracts", methods=["GET"])
def get_contracts():
    contracts_list = Contract.query.all()
    contracts_serialized = [contract.serialize() for contract in contracts_list]
    return jsonify(contracts_serialized), 200

# Get a contract by ID
@api.route("/contracts/<int:contract_id>", methods=["GET"])
def get_contract(contract_id):
    contract = Contract.query.filter_by(id=contract_id).first()
    if not contract:
        return jsonify({"msg":"Contract does not exist"}), 404
    return jsonify(contract.serialize()), 200

# Update a contract by ID
@api.route("/contracts/<int:contract_id>", methods=["PUT"])
def update_contract(contract_id):
    contract = Contract.query.filter_by(id=contract_id).first()
    if not contract:
        return jsonify({"msg":"Contract does not exist"}), 404
    data = request.json
    contract.terms = data.get("terms", contract.terms)
    contract.client_signature = data.get("client_signature", contract.client_signature)
    contract.contractor_signature = data.get("contractor_signature", contract.contractor_signature)
    db.session.commit()
    return jsonify({"msg":"contrat updated","result":contract.serialize()}), 200

# Delete a contract by ID
@api.route("/contracts/<int:contract_id>", methods=["DELETE"])
def delete_contract(contract_id):
    contract = Contract.query.filter_by(id=contract_id).first()
    if not contract:
        return jsonify({"msg":"Contract does not exist"}), 404
    db.session.delete(contract)
    db.session.commit()
    return jsonify({"msg": "Contract deleted successfully"}), 200


# choice:
# Create a new choice
@api.route("/choices", methods=["POST"])
def create_choice():
    data = request.json
    new_choice = Choice(
        project_id=data.get("project_id"),
        choice_type=data.get("choice_type"),
    )
    db.session.add(new_choice)
    db.session.commit()
    return jsonify({"msg":"choice created","result":new_choice.serialize()}), 201

# Get all choices
@api.route("/choices", methods=["GET"])
def get_choices():
    choices_list = Choice.query.all()
    choices_serialized = [choice.serialize() for choice in choices_list]
    return jsonify(choices_serialized), 200

# Get a choice by ID
@api.route("/choices/<int:choice_id>", methods=["GET"])
def get_choice(choice_id):
    choice = Choice.query.filter_by(id=choice_id).first()
    if not choice:
        return jsonify({"msg":"Choice does not exist"}), 404
    return jsonify(choice.serialize()), 200

# Update a choice by ID
@api.route("/choices/<int:choice_id>", methods=["PUT"])
def update_choice(choice_id):
    choice = Choice.query.filter_by(id=choice_id).first()
    if not choice:
        return jsonify({"msg":"Choice does not exist"}), 404
    data = request.json
    choice.choice_type = data.get("choice_type", choice.choice_type)
    db.session.commit()
    return jsonify({"msg":"choice updated!","result":choice.serialize()}), 200

# Delete a choice by ID
@api.route("/choices/<int:choice_id>", methods=["DELETE"])
def delete_choice(choice_id):
    choice = Choice.query.filter_by(id=choice_id).first()
    if not choice:
        return jsonify({"msg":"Choice does not exist"}), 404
    db.session.delete(choice)
    db.session.commit()
    return jsonify({"msg": "Choice deleted successfully"}), 200
