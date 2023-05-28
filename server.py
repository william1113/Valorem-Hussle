import json

from flask import Flask, redirect, render_template, request, session, url_for
from flask_login import LoginManager, login_required, current_user, logout_user, login_user

from flask_session import Session
from storePages import Pages
from tools.dbManger import DBManager, User
from tools.findNums import findNumsInString
from tools.webscraper import graber

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

@app.errorhandler(401)
def unauthorized(error):
    return render_template('unauthorized.html'), 401

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/", methods=["POST", "GET"])
@login_required
def index():
    if request.method == "POST":
        logout_user()
        return redirect(url_for("index"))
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    db_manager.addUserToDB()
        
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()
        if db_manager.checkPassword(email, password):
            login_user(user)  # Add this line to log in the user
            return redirect(url_for("index"))
        else:
            return "Invalid email or password"

    return render_template("login.html")

@app.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/results/", methods=["GET", "POST"])

@login_required
def results():
    search_query = findNumsInString(request.args.get("search_query"))
    if search_query:
        session["search_query"] = search_query
        data = graber(search_query)
        session["data"] = data
        return render_template("results.html", data=data, search_query=search_query)
    else:
        return redirect(url_for("search"))

@app.route("/search", methods=["POST"])
@login_required
def search():
  if request.method == "POST":
    search_query = findNumsInString(request.form['search_query'])
    session["search_query"] = search_query
    data = graber(search_query)
    session["data"] = data
    return redirect(url_for("results", search_query=search_query))
  else:
      return "404"
  
# Create the store page
Pages(app, 'kjell', "store1.html").createPage()

# Main entry point of the application
if __name__ == "__main__":
  db_manager.init_app(app)
  app.run(host='127.0.0.1', port=8080, debug=True)