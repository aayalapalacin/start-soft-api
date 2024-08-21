from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from enum import Enum

db = SQLAlchemy()



class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    role = db.Column(db.String(30), nullable=False)
    
    projects = db.relationship('Project', backref='client', lazy=True)
    tasks = db.relationship('Task', backref='contractor', lazy=True)

    def __repr__(self):
        return f'<User {self.name}>'
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "role": self.role,
        }

class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    client_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(30), default=StatusEnum.PENDING, nullable=False)
    is_completed = db.Column(db.Boolean, nullable=True)

    tasks = db.relationship('Task', backref='project', lazy=True)
    contract = db.relationship('Contract', backref='project', uselist=False)
    choice = db.relationship('Choice', backref='project', uselist=False)

    def __repr__(self):
        return f'<Project {self.name}>'
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "client_id": self.client_id,
            "status": self.status,
            "is_completed": self.is_completed,
        }

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    contractor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(30), default=StatusEnum.PENDING, nullable=False)
    is_completed = db.Column(db.Boolean, nullable=True)
 
    def __repr__(self):
        return f'<Task {self.name}>'
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "project_id": self.project_id,
            "contractor_id": self.contractor_id,
            "status": self.status,
            "is_completed": self.is_completed
        }

class Contract(db.Model):
    __tablename__ = 'contracts'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    contractor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    terms = db.Column(db.Text, nullable=False)
    client_signature = db.Column(db.Boolean, default=False, nullable=False)
    contractor_signature = db.Column(db.Boolean, default=False, nullable=False)
    def __repr__(self):
        return f'<Contract ProjectID={self.project_id}>'
    
    def serialize(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "contractor_id": self.contractor_id,
            "terms": self.terms,
            "client_signature": self.client_signature,
            "contractor_signature": self.contractor_signature,
        }

class Choice(db.Model):
    __tablename__ = 'choices'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    choice_type = db.Column(db.String(40), nullable=False)

    def __repr__(self):
        return f'<Choice {self.choice_type.value}>'
    
    def serialize(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "choice_type": self.choice_type
        }