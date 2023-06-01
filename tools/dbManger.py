import hashlib
import json
import os

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# database table for storing user information
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(256))
    salt = db.Column(db.String(1024))
    firstName = db.Column(db.String(50))
    lastName = db.Column(db.String(50))

    def get_id(self):
        return str(self.id)

# database table for storing the diffrent companies information
class Company(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(256))
    salt = db.Column(db.String(1024))
    
    companyName = db.Column(db.String(50))
    owner = db.Column(db.String(50))
    
    activity = db.Column(db.Integer)

# all the database tools
class DBManager:
    def init_app(self, app) -> None:
        db.init_app(app)
   
        with app.app_context():
            db.create_all()
    
            
    def addUserToDB(self, model, email="admin@gmail.com", password="123", firstName="admin", lastName="root", companyName=None, owner=None) -> bool:
        
        exists = self.checkForEmail(email, model)
        if exists:
            return True
        # user_requierments = ["email", "password", "firstName", "lastName"]
        hashed_password, salt = self.hashPassword(password, None, True)
        
        try:
            info = None
            
            if model == User:
                info = User(email=email, password=hashed_password, salt=salt, firstName=firstName, lastName=lastName)
            elif model == Company:
                info = Company(email=email, password=hashed_password, salt=salt, companyName=companyName, owner=owner)
            
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
        except CustomError as e:
            print(e)
            return False
    
    def updateData(self, CurrentEmail, model,**kwargs) -> bool:
        user = model.query.filter_by(email=CurrentEmail.lower()).first()
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

    def hashPassword(self, password, salt, newSalt=False):
        hashAmount = self.openConfigFile()["hashAmount"]

        if newSalt:
            salt = os.urandom(64)
            hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, hashAmount)
            return hashed_password, salt
        else:
            return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, hashAmount)
      
    def checkForEmail(self, email, model) -> bool:
        user = model.query.filter_by(email=email.lower()).first()
        if user is None:
            return False
        return True
  
    def checkPassword(self, email, password, model):
        user = model.query.filter_by(email=email.lower()).first()
        if user is None:
            return False
        hashed_password = self.hashPassword(password, user.salt, False)
      
        if user.password == hashed_password:
            return True
        else:
            return False
    
    def getUserData(self, email, model) -> dict:
        user = model.query.filter_by(email=email.lower()).first()
        if user is None:
            return {"status": False}
        
        column_names = [desc['name'] for desc in user.__class__.query.column_descriptions]
        user_data = {column_name : getattr(user, column_name) for column_name in column_names}
        return user_data
        
        

    
    def deleteUser(self, email, model):
        user = model.query.filter_by(email=email.lower()).first()
        db.session.delete(user)
  
    def openConfigFile(self) -> dict:
        with open("./config.json", "r") as config_file:
            return json.load(config_file)

# custom error handling
class CustomError(Exception):
    def __init__(self,message):
        self.message = message
    
    def __str__(self) -> str:
        return f"Error: {self.message}"