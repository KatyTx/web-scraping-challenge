# import necessary libraries
from flask import Flask, render_template, redirect
from pymongo import MongoClient

# From the separate python file in this directory, we'll import the code that is used to scrape craigslist
import mission_to_mars

# create instance of Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
#app.config["MONGO_URI"] = "mongodb://localhost:27017/craigslist_app"
mongo = MongoClient('mongodb://localhost:27017/mars_app')



# Render the index.html page with any craigslist listings in our database. 
# If there are no listings, the table will be empty.
@app.route("/")
def index():
    mars_results = mongo.db.mars_results.find_one()
    return render_template("index.html", mars=mars_results)

# This route will trigger the webscraping, but it will then send us back to the index route to render the results
@app.route("/scrape")
def scraper():

    mars_data = mission_to_mars.scrape()
    
    mongo.db.mars_results.update({},mars_data, upsert=True)
    # Use Flask's redirect function to send us to a different route once this task has completed.
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)