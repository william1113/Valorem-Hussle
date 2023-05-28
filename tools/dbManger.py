from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
import hashlib
import os
db = SQLAlchemy()
# Define the User model


# Define the DBManager
class DBManger:
  def init_app(self, app) -> None: # initialize application
      db.init_app(app)
      with app.app_context():
          db.create_all()
  
  def addUserToDB(self, email="admin@gmail.com", password="123", firstName="admin", lastName="root") -> bool:
      exists = self.checkForEmail(email)
      if exists:
          return True
      
      hashed_password,salt = self.hashPassword(password, None,True)  
      info = User(email=email, password=hashed_password, salt=salt, firstName=firstName, lastName=lastName)
      
      db.session.add(info)
      db.session.commit()
      
      return False

  def hashPassword(self, password, salt, newSalt = False): # returns hash of password and or salt
      hashAmount = self.openConfigFile()["hashAmount"]

      if newSalt:
          salt = os.urandom(64)
          hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, hashAmount)
          return hashed_password, salt
      else:
          return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, hashAmount)
      
  def checkForEmail(self, email) -> bool: # when a new user is trying to create an account
      user = User.query.filter_by(email=email).first()
      if user is None:
          return False
      return True
  
  def checkPassword(self, email, password): #only happens when user is trying to login in
      user = User.query.filter_by(email=email).first()
      if user is None:
          return False
      hashed_password = self.hashPassword(password, user.salt,False)
      
      if user.password == hashed_password:
          return True
      else:
          return False
  
  def printDataBase(self) -> None: #prints out the data base in the terminal
      users = User.query.all()
      
      for user in users:
          print(f"id: {user.id} | Email: {user.email} | Password : {user.password} | first name: {user.firstName} | last name: {user.lastName}")
  
  def getData(self, email) -> dict: # returns dict with the user data
      user = User.query.filter_by(email=email).first()
      return {
          "id": user.id,
          "email": user.email,
          "password": user.password,
          "salt": user.salt,
          "firstName": user.firstName,
          "lastName": user.lastName
      }
      
  def updateData(self,CurrentEmail ,**kwargs) -> bool: # updates the user data
      user = db.session.query(User).filter_by(email=CurrentEmail).first()
      if user:
          for key, value in kwargs.items():
              setattr(user, key, value)
  
          db.session.commit()
          return True
      return False
  
  def openConfigFile(self) -> dict: # returns data from config file
    return {
  "dbURL": "sqlite:///userdata.db",
  "SECRET_KEY": "u+3tknB8M>]-}@K3)8o=5m#rGH-jt@j.k8qk,V%Vzn%vo4m^:C!CbXCo7k%R*ek.0nEoydhMt}g7M?3GZ#,5}Ezprx5z1impcg,-",
  "hashAmount": 20000
}

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(256))
    salt = db.Column(db.String(1024))
    firstName = db.Column(db.String(50))
    lastName = db.Column(db.String(50))