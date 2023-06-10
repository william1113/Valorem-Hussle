import base64
import json

from flask import (Flask, flash, redirect, render_template, request, session,
                   url_for)
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

from flask_session import Session
from tools.dbManger import Company, DBManager, User, db, CompanyProducts
from tools.storePages import Pages
from tools.validation import validatorFunc
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
#error handeler
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
    print(current_user)
    db_manager.addUserToDB(User, email="admin@gmail.com", password="admin", name="admin")
    db_manager.addUserToDB(Company, email="root@gmail.com", password="root", owner="root", company_name ="root")    
    if request.method == "POST":
        email = request.form["email"]                               
        password = request.form["password"]
        
        user = User.query.filter_by(email=email).first()
 
        if user is None:
            user = Company.query.filter_by(email=email).first()
            
        
        if db_manager.checkPassword(email, password, User) or db_manager.checkPassword(email, password, Company):
            login_user(user)  # Add this line to log in the user
            session["email"] = user.email
            user_ip = request.remote_addr
            print(f"User: {user.email} just logged in successfully with IP: {user_ip}")
    
            return redirect(url_for("index"))
        else:
            return "Invalid email or password"
    else:
        return render_template("login.html")

#creates the function so user can logout
@app.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

#register new user page
@app.route("/register-user", methods=["GET"])
def register_user():
    return render_template("registerUser.html")


#adds the user  to the database
@app.route("/register/user-data", methods=["POST"])
def register_user_profile():

    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]
    
    print(validatorFunc(name=name, email=email, password=password, company=False),1000)

    if validatorFunc(name=name, email=email, password=password, company=False):
        status = db_manager.addUserToDB(User,email=email, password=password, name=name)

        if status is False:
            user_ip = request.remote_addr
            
            print(f"User: {email} just registerd successfully with IP: {user_ip}")
            return redirect(url_for("login"))
    print("here")
    return redirect(url_for("registerUser", status=404))

@app.route("/register/company", methods=["GET"])
def register_company():
    return render_template("registerCompany.html")

@app.route("/register/company/data", methods=["POST"])
def register_company_profile():
    
    email = request.form["email"]
    password = request.form["password"]
    owner = request.form["owner"]
    company_name = request.form["companyName"]
    
    if validatorFunc(email=email, password=password, name=owner, company=company_name):
    
        status = db_manager.addUserToDB(Company,email=email, password=password, owner=owner, company_name=company_name)
        if status is False:
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
    # Get the company details
    company_details = Company.query.filter_by(email=session["email"]).first()

    # Get all products associated with the company
    products = CompanyProducts.query.filter_by(company_id=company_details.id).all()
    print(products)
    return render_template("companyprofile.html", company=company_details, products=products)
@app.route("/updateProfileData/", methods=["POST"])
@login_required
def updateProfileData():
    image = request.files["image"].read()  # Read the image data from the uploaded file
    link = request.form["link"]
    text = request.form["text"]
    price = request.form["price"]
    #print(company_name)
    image_data_base64 = base64.b64encode(image).decode('utf-8')
    # Check if a product with the provided criteria already exists
    product = CompanyProducts.query.filter_by(link=link, text=text, price=price).first()
    companyDetails = Company.query.filter_by(email=session["email"]).first().id
    
    if product:
        # If the product already exists, update its image
        product.image_data = image
    else:
        # If the product doesn't exist, create a new instance and assign the values
        product = CompanyProducts()
        product.image_data = image_data_base64
        product.link = link
        product.text = text
        product.price = price
        product.company_id = companyDetails 
        # Add the product to the session
        db.session.add(product)

    # Commit the changes to the database
    db.session.commit()

    return redirect(url_for("updateprofile"))


# Create the store page
Pages(app, 'kjell', "store1.html").createPage()

# Main entry point of the application
if __name__ == "__main__":
    db_manager.init_app(app)
    app.run(host="127.0.0.1", port=5500, debug=True)