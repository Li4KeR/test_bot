from app import app
from flask import render_template


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/", methods=["POST"])
def index_post():
    pass


@app.route("/create_master", methods=["POST"])
def create_master():
    pass

