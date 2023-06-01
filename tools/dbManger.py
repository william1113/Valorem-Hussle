import hashlib
import json
import os

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError, NoResultFound

db = SQLAlchemy()


# database table for storing user information
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(256))
    salt = db.Column(db.String(1024))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))

    def get_id(self):
        return str(self.id)

# database table for storing the different companies information
class Company(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(256))
    salt = db.Column(db.String(1024))
    
    company_name = db.Column(db.String(50))
    owner = db.Column(db.String(50))
    
    activity = db.Column(db.Integer)

# all the database tools
class DBManager:
    def init_app(self, app) -> None:
        db.init_app(app)
   
        with app.app_context():
            db.create_all()
    
            
    def add_user_to_db(self, model, email="admin@gmail.com", password="123", first_name="admin", last_name="root", company_name=None, owner=None) -> bool:
        if model == User:
            exists = self.check_for_email(email, model)
        else:
            exists = self.check_for_email(email, model, company_name)
        if exists:
            return True
        # user_requirements = ["email", "password", "first_name", "last_name"]
        hashed_password, salt = self.hash_password(password, None, True)
        
        try:
            info = None
            
            if model == User:
                info = User(email=email, password=hashed_password, salt=salt, first_name=first_name, last_name=last_name)
            elif model == Company:
                info = Company(email=email, password=hashed_password, salt=salt, company_name=company_name, owner=owner)
            
            """
            if model == User:
                for key, value in kwargs.items():
                    setattr(User, key, value)
            
            setattr(User, "password", hashed_password)
            setattr(User, "salt", salt)
            """    
            
            
            db.session.add(info)
            db.session.commit()
            return True
        except IntegrityError:
            return False
    
    def update_data(self, current_email, model, **kwargs) -> bool:
        user = model.query.filter_by(email=current_email).first()
        if user:
            for key, value in kwargs.items():
                setattr(user, key, value)
            try:
                db.session.commit()
                raise CustomError("Table not found")
            except CustomError as e:
                print(e)
            
            return True
        return False

    def hash_password(self, password, salt, new_salt=False):
        hash_amount = self.open_config_file()["hashAmount"]

        if new_salt:
            salt = os.urandom(64)
            hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, hash_amount)
            return hashed_password, salt
        else:
            return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, hash_amount)
      
    def check_for_email(self, email, model, company_name=None) -> bool:
        try:
            user = model.query.filter_by(email=email).first()
            if user:
                if model == Company:
                    name = Company.query.filter_by(company_name=company_name).first()
                    if name:
                        return True
                return True
            return False
        except NoResultFound:
            return False
    
    def check_for_company_name(self, company_name) -> bool:
        try:
            user = Company.query.filter_by(name=company_name).first()
            
            if user:
                return True
            return False
        except NoResultFound:
            return False
  
    def check_password(self, email, password, model):
        user = model.query.filter_by(email=email).first()
        if user is None:
            return False
        hashed_password = self.hash_password(password, user.salt, False)
      
        if user.password == hashed_password:
            return True
        else:
            return False
    
    def get_user_data(self, email, model) -> dict:
        user = model.query.filter_by(email=email.lower()).first()
        if user is None:
            return {"status": False}
        
        column_names = [desc['name'] for desc in user.__class__.query.column_descriptions]
        user_data = {column_name: getattr(user, column_name) for column_name in column_names}
        return user_data
        
        

    
    def delete_user(self, email, model):
        user = model.query.filter_by(email=email.lower()).first()
        db.session.delete(user)
  
    def open_config_file(self) -> dict:
        with open("./config.json", "r") as config_file:
            return json.load(config_file)

# custom error handling
class CustomError(Exception):
    def __init__(self, message):
        self.message = message
    
    def __str__(self) -> str:
        return f"Error: {self.message}"