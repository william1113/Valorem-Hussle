import json
from flask import Flask, redirect, render_template, request, session, url_for

from tools.dbManger import DBManger
from tools.webscraper import graber
from storePages import Pages

# sets the default settings 
with open ("config.json", "r") as config_file:
    config = json.load(config_file)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config["dbURL"]
app.secret_key = config['SECRET_KEY']
#db_manager = DBManger()

#----------------------------------------------------------------




def remove_non_ascii(text):
    return text.encode().decode('unicode_escape')


    
@app.route("/", methods = ["POST", "GET"])
def index(): # inialtzes the front page also called the home page
    return render_template("index.html")

@app.route("/results", methods = ["POST"])
def search():
    search_query = request.form['search_query']
    data = graber(search_query)
 
    
    return render_template("results.html", data=data, search_query=search_query)    


@app.route("/results", methods=["GET", "POST"])
def results():
    return render_template("results.html")



page1 = Pages(app, 'kjell', "store1.html")
page1.createPage()

# runs the server for the webpages and also the database server
if __name__ == "__main__":

    #db_manager.init_app(app)
    app.run(host='127.0.0.1', port=8080)
  
   