import flask
import json
from flask import render_template , jsonify , request , url_for
from datetime import datetime


app = flask.Flask("Online Store")

def load_products():
    file = open('products.json', 'r')
    products = json.load(file)
    return products

def save_products(products):
    file = open('products.json', 'w')
    json.dump(products, file)

class Product:
    def __init__(self , id , image ,  name , price , description , stock):
        
        self.id = id
        self.image = image
        self.name = name
        self.price = price
        self.description = description
        self.stock = stock

    def discount(self , discount_percentage):
        self.price = self.price * (100 - discount_percentage) / 100

    def update_stock (self , quantity):
        try:
            new_stock = self.stock + quantity

            if new_stock < 0:
                return "Stock quantity can not be negative"
            
            self.stock = new_stock 
            return "Stock updated successfully."
        except:
            return "Quantiy must be a number"

@app.route("/")
def home():
    offer_end_time = datetime(2024 , 3 , 30 , 23 , 59 , 59)
    now = datetime.now()
    time_remaining = offer_end_time - now
    remaining_seconds = int(time_remaining.total_seconds())
    days = remaining_seconds // (24*3600)
    remaining_seconds = remaining_seconds % (24*3600)
    hours = remaining_seconds // (3600)
    remaining_seconds = remaining_seconds % 3600
    minutes = remaining_seconds // 60
    seconds = remaining_seconds % 60
    products = load_products()
    return render_template("index.html" , days =days , hours = hours , minutes = minutes , seconds = seconds , products=products)

# @app.route("/products")
# def get_products():
#     products = load_products()
#     return render_template("index.html", products=products)

@app.route('/product/<product_id>')
def product_detail(product_id):
    products = load_products()
    product = None
    for p in products:
        if str(p['id']) == product_id:
            product = p
            break

    if product:
        return render_template('product_detail.html', product=product)
    else:
        return "Product not found"