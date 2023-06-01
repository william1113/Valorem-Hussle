import json

from flask import Flask, redirect, render_template, request, session, url_for
from flask_login import LoginManager, login_required, login_user, logout_user

from flask_session import Session
from tools.dbManger import Company, DBManager, User, db
from tools.storePages import Pages
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

user_counter = 0

# Error handler for error code 401
def handle_error(error):
    error_code = getattr(error, 'code', 500)
    print(error_code)
    return render_template("unauthorized.html")

@app.errorhandler(Exception)
def unauthorized(error):
    return handle_error(error)

# Load the user through user id
@login_manager.user_loader
def load_user(user_id):
    user = db.session.get(User, int(user_id))
    if not user:
        user = db.session.get(Company, int(user_id))
    return user

# Main page for the website
@app.route("/", methods=["POST", "GET"])
@login_required
def index():
    if request.method == "POST":
        logout_user()
        return redirect(url_for("index"))
    return render_template("index.html")

# Login page
@app.route("/login", methods=["GET", "POST"])
def login():
    # Test user
    db_manager.add_user_to_db(User)
    
    # Handle login request
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        
        user = User.query.filter_by(email=email).first()
        if user is None:
            user = Company.query.filter_by(email=email).first()
        
        if db_manager.check_password(email, password, User):
            login_user(user)  # Add this line to log in the user
            user_ip = request.remote_addr
            print(f"User: {user.email} just logged in successfully with IP: {user_ip}")
            return redirect(url_for("index"))
        else:
            return "Invalid email or password"

    return render_template("login.html")

# Logout route
@app.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

# Register new user page
@app.route("/register/user", methods=["GET"])
def register_user():
    return render_template("registerUser.html")

# Register new company page
@app.route("/register/company", methods=["GET"])
def register_company():
    return render_template("registerCompany.html")

# registers new user to database
@app.route("/addUser", methods=["POST"])
def register_user_profile():
    first_name = request.form["firstname"]
    last_name = request.form["lastname"]
    email = request.form["email"]
    password = request.form["password"]
    
    res = db_manager.add_user_to_db(User, email=email, password=password, first_name=first_name, last_name=last_name)
    
    if res:
        user_ip = request.remote_addr
        print(f"User: {email} just registered successfully with IP: {user_ip}")
        return redirect(url_for("login"))
    return redirect(url_for("register/user", status="Account already exists"))

# registers a new company to the database
@app.route("/addCompany", methods=["POST"])
def register_company_profile():
    email = request.form["email"]
    password = request.form["password"]
    owner = request.form["owner"]
    company_name = request.form["companyName"]
    
    status = db_manager.add_user_to_db(Company, email=email, password=password, owner=owner, company_name=company_name)
    if status:
        return redirect(url_for("login"))
    else:
        return redirect(url_for("registerCompany", status="Company already exists"))
    
@app.route("/check-for-company", methods=["POST"])
def check_for_company():
    
    return {}

# Search with the help of search query and web scraper
@app.route("/search", methods=["POST"])
@login_required
def search():
    if request.method == "POST":
        search_query = request.form['search_query']
        session["search_query"] = search_query
        data = graber(search_query)
        session["data"] = data
        return redirect(url_for("results", search_query=search_query))
    else:
        return "404"

# Results page for the search bar
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

@app.route("/updateprofile/", methods=["GET", "POST"])
@login_required
def update_profile():
    return render_template("updateprofile.html")

@app.route("/updateProfileData/", methods=["POST"])
def update_profile_data():
    return redirect(url_for("updateprofile", data=session["first_name"]))

# Track the number of users on the web app
def increment_user_counter():
    global user_counter
    user_counter += 1

def decrement_user_counter():
    global user_counter
    user_counter -= 1

@app.before_request
def before_request():
    if "active" in session:
        increment_user_counter()

@app.after_request
def after_request(response):
    if "active" in session:
        decrement_user_counter()
    return response

# Create the store page
Pages(app, 'kjell', "store1.html").create_page()

# Main entry point of the application
if __name__ == "__main__":
    db_manager.init_app(app)
    app.run(host="127.0.0.1", port=5500, debug=True)