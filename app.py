import json
from flask import Flask , render_template , request , session , url_for ,redirect
from datetime import datetime


app = Flask("Online Store")


class Product:
    def __init__(self , id , image ,  name , price , description , stock , quantity):
        
        self.id = id
        self.image = image
        self.name = name
        self.price = price
        self.description = description
        self.stock = stock
        self.quantity = quantity

    def total_price(self):
        return self.price * self.quantity

# def load_products(filename):
#     file = open(filename, 'r')
#     products = json.load(file)
#     return products

def load_products(filename):
    file = open(filename, 'r')
    products_data = json.load(file)
    file.close()
    products = []
    for p in products_data:
        product = Product(p['id'], p['image'], p['name'], p['price'], p['description'], p['stock'], p['quantity'])
        products.append(product)

    return products


def save_products(cart):
    file = open('cart.json', 'w')
    json.dump(cart, file)
    file.close()
        

def time_to_offer():
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
    return days , hours , minutes , seconds

@app.route("/")
def home():
    days , hours , minutes , seconds = time_to_offer()
    products = load_products("products.json")
    return render_template("index.html" , days =days , hours = hours , minutes = minutes , seconds = seconds , products=products)

# @app.route("/products")
# def get_products():
#     products = load_products()
#     return render_template("index.html", products=products)

@app.route('/product/<product_id>')
def product_detail(product_id):
    days , hours , minutes , seconds = time_to_offer()
    products = load_products("products.json")
    product = None
    for p in products:
        if str(p.id) == product_id:
            product = p
            break

    if product:
        return render_template('product_detail.html', days =days , hours = hours , minutes = minutes , seconds = seconds , product=product)
    else:
        return "Product not found"
    

@app.route("/search")
def search_products():
    days , hours , minutes , seconds = time_to_offer()
    product_to_find = request.args.get("product_to_find")
    product_to_find = product_to_find.lower()
    products = load_products("products.json")
    filtered_product = None
    for p in products:
        if p.name.lower() == product_to_find:
            filtered_product = p
    if (filtered_product):
        return render_template("product_detail.html" , product = filtered_product , days =days , hours = hours , minutes = minutes , seconds = seconds)
    else:
        return render_template("index.html" , days =days , hours = hours , minutes = minutes , seconds = seconds , products=products)


@app.route("/add-to-cart/<product_id>", methods=['POST'])
def add_to_cart(product_id):
    try:
        file = open('cart.json', 'r')
        cart = json.load(file)
        file.close()
    except:
        cart = {"items": []}

    try:
        products = load_products("products.json")
        product = None
        for p in products:
            if str(p.id) == product_id:
                product = p
                break

        selected_quantity = int(request.form.get("quantity"))
        product.quantity = selected_quantity

        for item in cart['items']:
            if str(item['id']) == product_id:
                item['quantity'] = selected_quantity
                item['price'] = product.total_price()
                break
                
        else:
            cart['items'].append({
                'id': product.id, 
                'name': product.name,
                'image': product.image , 
                'price': product.total_price(), 
                'quantity': selected_quantity
            })

        save_products(cart)

    except:
        return "An error occurred"

    return redirect(url_for("show_cart"))

@app.route("/remove-from-cart/<product_id>" , methods=["POST"])
def remove_from_cart(product_id):
    try:
        file = open('cart.json', 'r')
        cart = json.load(file)
        file.close()

        updated_cart_items = []

        for item in cart['items']:
            if str(item['id']) != product_id:
                updated_cart_items.append(item)

        cart['items'] = updated_cart_items

        save_products(cart)

    except:
        return "An error occurred"

    return redirect(url_for("show_cart"))

@app.route('/cart')
def show_cart():
    file = open('cart.json', 'r')
    cart = json.load(file)
    file.close()

    return render_template('cart.html', cart_items=cart['items'])