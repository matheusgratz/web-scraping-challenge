from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


@app.route("/")
def index():
    Mars = mongo.db.Mars.find_one()
    return render_template("index.html", mars=Mars)


@app.route("/scrape")
def scraper():
    Mars = mongo.db.Mars
    Mars_Dict = scrape.get_everything()
    Mars.update({}, Mars_Dict, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)