import json
from flask import Flask, redirect, render_template, url_for, request, session 
from flask_session import Session

from tools.dbManger import DBManger
from tools.webscraper import graber
from tools.findNums import findNumsInString
from storePages import Pages

# sets the default settings 
with open ("config.json", "r") as config_file:
    config = json.load(config_file)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config["dbURL"]
app.secret_key = config['SECRET_KEY']


#db_manager = DBManger()

#----------------------------------------------------------------

@app.route("/", methods=["POST", "GET"])
def index():
    return render_template("index.html")


@app.route(f"/results/", methods=["GET", "POST"])
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
def search():
    search_query = findNumsInString(request.form['search_query'])
    session["search_query"] = search_query
    data = graber(search_query)
    session["data"] = data
    return redirect(url_for("results", search_query=search_query))
    


Pages(app, 'kjell', "store1.html").createPage()

# runs the server for the webpages and also the database server
if __name__ == "__main__":
    #db_manager.init_app(app)
    app.run(host='127.0.0.1', port=8080)
  
   