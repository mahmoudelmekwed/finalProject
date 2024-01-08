import flask
from flask import render_template
from datetime import datetime

app = flask.Flask("Online Store")

@app.route("/")
def home():
    offer_end_time = datetime(2024 , 3 , 30 , 23 , 59 , 59)
    now = datetime.now()
    time_remaining = offer_end_time - now
    remaining_seconds = time_remaining.total_seconds()
    days = remaining_seconds // (24*3600)
    remaining_seconds = remaining_seconds % (24*3600)
    hours = remaining_seconds // (3600)
    remaining_seconds = remaining_seconds % 3600
    minutes = remaining_seconds // 60
    seconds = remaining_seconds % 60
    return render_template("index.html" , days = days , hours = hours , minutes = minutes , seconds = seconds)
