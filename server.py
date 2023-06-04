import asyncio

import re
import json

from flask import Flask, redirect, render_template, request, session, url_for, flash
from flask_login import LoginManager, login_required, logout_user, login_user

from flask_session import Session
from tools.storePages import Pages
from tools.dbManger import DBManager, User, Company, db
from tools.webscraper import graber
from tools.validation import *
app = Flask(__name__)


# Load configuration from config.json
with open("config.json", "r") as config_file:
    config = json.load(config_file)

# Configure Flask app
app.config['SQLALCHEMY_DATABASE_URI'] = config["dbURL"]
app.secret_key = config['SECRET_KEY']
app.config['SESSION_TYPE'] = 'filesystem'

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Configure Flask-Session
Session(app)

# Create an instance of the DBManager
db_manager = DBManager()


user_counter = 0
#error handel for error code 401




def handle_error(error):
    error_code = getattr(error, 'code', 500)
    print(error_code)
    return render_template("unauthorized.html")

@app.errorhandler(Exception)
def unauthorized(error):
    return handle_error(error)


#loads the user through user id
@login_manager.user_loader
def load_user(user_id):
    user = db.session.get(User, int(user_id))
    if not user:
        user = db.session.get(Company, int(user_id))
    
    return user
    
#main page for website
@app.route("/", methods=["POST", "GET"])

@login_required
def index():
    if request.method == "POST":
        logout_user()
        return redirect(url_for("index"))
    return render_template("index.html")

#login page 
@app.route("/login", methods=["GET", "POST"])
def login():
    #test user
    db_manager.addUserToDB(User)    #----------------------------------------------------------------
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        
        user = User.query.filter_by(email=email).first()
        if user is None:
            user = Company.query.filter_by(email=email).first()
        
        
        if db_manager.checkPassword(email, password, User):
            login_user(user)  # Add this line to log in the user
            user_ip = request.remote_addr
            print(f"User: {user.email} just logged in successfully with IP: {user_ip}")
            return redirect(url_for("index"))
        else:
            return "Invalid email or password"

    return render_template("login.html")

#creates the function so user can logout
@app.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

#register new user page
@app.route("/register-user", methods=["GET"])
def registerUser():
    return render_template("registerUser.html")


#adds the user to the database




@app.route("/register/user-data", methods=["POST"])
def registerUserProfile():

    name = request.form["firstname"]
    email = request.form["email"]
    password = request.form["password"]
    
    validation_functions = { "email": (email,is_valid_email),
    "password": (password,is_valid_password),
    "Name": (name, is_valid_name)}
    
    validator: bool = False
    
    for value in validation_functions:
        validator = validation_functions[value][1](validation_functions[value][0])
        #print(validator, value)
        if validator:
            continue 
        else:
            validator = False
            break

    if validator:
        res = db_manager.addUserToDB(User,email, password, name)
        print("Result db check",res)
        if res == False:
            user_ip = request.remote_addr
            
            print(f"User: {email} just registerd successfully with IP: {user_ip}")
            return redirect(url_for("login"))
    print("here")
    return redirect(url_for("registerUser", status=404))

@app.route("/register/company", methods=["GET"])
def registerCompany():
    return render_template("registerCompany.html")

@app.route("/register/company/data", methods=["POST"])
def registerCompanyProfile():
    email = request.form["email"]
    password = request.form["password"]
    owner = request.form["owner"]
    company_name = request.form["companyName"]
    
    validation_functions = { "email": (email,is_valid_email),
    "password": (password,is_valid_password),
    "Name": (owner, is_valid_name),
    "Company Name": (company_name,is_valid_company_name)}
    
    if any(func(value) for value, func in validation_functions.values()):
    
        status = db_manager.addUserToDB(Company,email, password, owner, company_name)
        if status:
            return redirect(url_for("login"))
        else:
            flash("Company already exists")
            return redirect(url_for("registerCompany"))
    return redirect(url_for("register/company"))




#searches with the help of search query and webscraper
@app.route("/search", methods=["POST"])
@login_required
def search():
  if request.method == "POST":
    # search_query = findNumsInString(request.form['search_query'])
    search_query = request.form['search_query']
    session["search_query"] = search_query
    data = graber(search_query)
    session["data"] = data
    return redirect(url_for("results", search_query=search_query))
  else:
      return "404"

#results page for the search bar
@app.route("/results/", methods=["GET", "POST"])
@login_required
def results():

    search_query = request.args.get("search_query")
    if search_query:
        session["search_query"] = search_query
        data = graber(search_query)
        session["data"] = data
        return render_template("results.html", data=data, search_query=search_query)
    else:
        return redirect(url_for("search"))
    
@app.route("/home", methods=["GET", "POST"])
def home():
    return render_template("home.html")

@login_required
@app.route("/updateprofile/", methods=["GET", "POST"])
def updateprofile():
    return render_template("updateprofile.html")

@app.route("/updateProfileData/", methods=["GET","POST", "DELETE", "PUT"])
def updateProfileData():
    
    return redirect(url_for("updateprofile", data=session["firstName"]))



# Create the store page
Pages(app, 'kjell', "store1.html").createPage()

# Main entry point of the application
if __name__ == "__main__":
    db_manager.init_app(app)
    app.run(host="127.0.0.1", port=5500, debug=True)