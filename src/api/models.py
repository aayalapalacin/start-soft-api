from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from enum import Enum

db = SQLAlchemy()

# Enum for role in Users table
class UserRole(Enum):
    CLIENT = 'client'
    CONTRACTOR = 'contractor'

# Enum for status in Projects and Tasks tables
class StatusEnum(Enum):
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'

# Enum for choice type in Choices table
class ChoiceType(Enum):
    INSURANCE_SALES = 'Insurance sales'
    WEB_DESIGN = 'Web design'
    BUSINESS_DEV_MARKETING = 'Business development and marketing'
    REAL_ESTATE = 'Real estate'

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    role = db.Column(db.Enum(UserRole), nullable=False)
    
    projects = db.relationship('Project', backref='client', lazy=True)
    tasks = db.relationship('Task', backref='contractor', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    client_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.Enum(StatusEnum), default=StatusEnum.PENDING, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completion_date = db.Column(db.DateTime, nullable=True)

    tasks = db.relationship('Task', backref='project', lazy=True)
    contract = db.relationship('Contract', backref='project', uselist=False)
    choice = db.relationship('Choice', backref='project', uselist=False)

    def __repr__(self):
        return f'<Project {self.name}>'

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    contractor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.Enum(StatusEnum), default=StatusEnum.PENDING, nullable=False)
    completion_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Task {self.name}>'

class Contract(db.Model):
    __tablename__ = 'contracts'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    contractor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    terms = db.Column(db.Text, nullable=False)
    client_signature = db.Column(db.Boolean, default=False, nullable=False)
    contractor_signature = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Contract ProjectID={self.project_id}>'

class Choice(db.Model):
    __tablename__ = 'choices'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    choice_type = db.Column(db.Enum(ChoiceType), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Choice {self.choice_type.value}>'