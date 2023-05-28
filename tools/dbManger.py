from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
import hashlib
import os

db = SQLAlchemy()

# Define the User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(256))
    salt = db.Column(db.String(1024))
    firstName = db.Column(db.String(50))
    lastName = db.Column(db.String(50))

    def get_id(self):
        return str(self.id)

# Define the DBManager
class DBManager:
    def init_app(self, app) -> None:
        db.init_app(app)
        with app.app_context():
            db.create_all()
  
    def addUserToDB(self, email="admin@gmail.com", password="123", firstName="admin", lastName="root") -> bool:
        exists = self.checkForEmail(email)
        if exists:
            return True
      
        hashed_password, salt = self.hashPassword(password, None, True)  
        info = User(email=email, password=hashed_password, salt=salt, firstName=firstName, lastName=lastName)
      
        db.session.add(info)
        db.session.commit()
      
        return False

    def hashPassword(self, password, salt, newSalt=False):
        hashAmount = self.openConfigFile()["hashAmount"]

        if newSalt:
            salt = os.urandom(64)
            hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, hashAmount)
            return hashed_password, salt
        else:
            return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, hashAmount)
      
    def checkForEmail(self, email) -> bool:
        user = User.query.filter_by(email=email.lower()).first()
        if user is None:
            return False
        return True
  
    def checkPassword(self, email, password):
        user = User.query.filter_by(email=email.lower()).first()
        if user is None:
            return False
        hashed_password = self.hashPassword(password, user.salt, False)
      
        if user.password == hashed_password:
            return True
        else:
            return False
  
    def printDataBase(self) -> None:
        users = User.query.all()
      
        for user in users:
            print(f"id: {user.id} | Email: {user.email} | Password : {user.password} | first name: {user.firstName} | last name: {user.lastName}")
  
    def getData(self, email) -> dict:
        user = User.query.filter_by(email=email.lower()).first()
        return {
            "id": user.id,
            "email": user.email,
            "password": user.password,
            "salt": user.salt,
            "firstName": user.firstName,
            "lastName": user.lastName
        }
      
    def updateData(self, CurrentEmail, **kwargs) -> bool:
        user = User.query.filter_by(email=CurrentEmail.lower()).first()
        if user:
            for key, value in kwargs.items():
                setattr(user, key, value)
  
            db.session.commit()
            return True
        return False
  
    def openConfigFile(self) -> dict:
        return {
            "dbURL": "sqlite:///userdata.db",
            "SECRET_KEY": "u+3tknB8M>]-}@K3)8o=5m#rGH-jt@j.k8qk,V%Vzn%vo4m^:C!CbXCo7k%R*ek.0nEoydhMt}g7M?3GZ#,5}Ezprx5z1impcg,-",
            "hashAmount": 20000
        }