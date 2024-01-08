import flask
from flask import render_template

app = flask.Flask("Online Store")

@app.route("/")
def home():
    return render_template("index.html")
