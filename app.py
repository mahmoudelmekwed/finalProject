import json
from flask import Flask, jsonify, render_template , request, session , url_for ,redirect
import secrets


app = Flask("Online Store")
app.secret_key = secrets.token_hex(16)


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
        return round(self.price * self.quantity , 2 ) 
    
class User:
    def __init__(self, username , password , email , address, payment_method , payment_details):
        self.username = username
        self.password = password
        self.email = email
        self.address = address
        self.payment_method = payment_method
        self.payment_details = payment_details


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

@app.route("/")
def home():
    products = load_products("products.json")
    return render_template("index.html" , products=products)

@app.route('/product/<product_id>')
def product_detail(product_id):
    products = load_products("products.json")
    product = None
    for p in products:
        if str(p.id) == product_id:
            product = p
            break

    if product:
        return render_template('product_detail.html', product=product)
    else:
        return "Product not found"
    

@app.route("/search")
def search_products():
    product_to_find = request.args.get("product_to_find")
    product_to_find = product_to_find.lower()
    products = load_products("products.json")
    filtered_products = []
    for p in products:
        if product_to_find in p.name.lower():
            filtered_products.append(p)
    
###################################################################
    return render_template("search.html" , products = filtered_products , product_to_find = product_to_find)

@app.route("/add-to-cart/<product_id>", methods=['POST'])
def add_to_cart(product_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    try:
        file = open('cart.json', 'r')
        cart = json.load(file)
        file.close()
    except:
        cart = {}

    user_cart = cart.get(username, {"items": []})

    try:
        products = load_products("products.json")
        product = None
        for p in products:
            if str(p.id) == product_id:
                product = p
                break
    
        if product:
            selected_quantity = int(request.form.get("quantity"))
            product.quantity = selected_quantity

        for item in user_cart['items']:
            if str(item['id']) == product_id:
                item['quantity'] = selected_quantity
                item['price'] = product.total_price()
                break
                
        else:
            user_cart['items'].append({
                'id': product.id, 
                'name': product.name,
                'image': product.image , 
                'price': product.total_price(),
                'description' : product.description, 
                'quantity': selected_quantity
            })

        cart[username] = user_cart

        save_products(cart)

    except:
        return "An error occurred"

    return redirect(url_for("show_cart"))

@app.route("/remove-from-cart/<product_id>" , methods=["POST"])
def remove_from_cart(product_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    try:
        file = open('cart.json', 'r')
        cart = json.load(file)
        file.close()

        user_cart = cart.get(username, {"items": []})

        updated_cart_items = []

        for item in user_cart['items']:
            if str(item['id']) != product_id:
                updated_cart_items.append(item)

        user_cart['items'] = updated_cart_items
        cart[username] = user_cart

        save_products(cart)

    except:
        return "An error occurred"

    return redirect(url_for("show_cart"))

###############################################################################################

def calculate_cart_total(cart):
    total = 0
    for item in cart['items']:
        total += item['price']
    return round(total , 2 )

@app.route('/cart')
def show_cart():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']

    file = open('cart.json', 'r')
    cart = json.load(file)
    file.close()
    
    user_cart = cart.get(username, {"items": []})

    total_price = calculate_cart_total(user_cart)
    session['total_price'] = total_price

    return render_template('cart.html', cart_items=user_cart['items'] , total_price = total_price)

#######################################################

@app.route('/checkout')
def checkout():

    total_price = session.get('total_price' , 0)
    return render_template('checkout.html' , total_price = total_price)



###########################################################################################################################

def save_user(user):
    try:
        with open('users.json', 'r') as file:
            users = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        users = []

    user_data = {
        'username': user.username,
        'password': user.password,
        'email' : user.email ,
        'address': user.address,
        'payment_method': user.payment_method,
        'payment_details': user.payment_details
    }

    users.append(user_data)

    with open('users.json', 'w') as file:
        json.dump(users, file)

def retrieve_user(identifier):
    try:
        with open('users.json', 'r') as file:
            users = json.load(file)
            for user_data in users:
                if user_data['username'] == identifier or user_data['email'] == identifier:
                    return User(
                        username=user_data['username'], 
                        password=user_data['password'],
                        email =user_data['email'],
                        address=user_data['address'], 
                        payment_method=user_data['payment_method'], 
                        payment_details=user_data['payment_details']
                    )
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return None

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'] 
        email = request.form['email'] 
        # if retrieve_user(email):
        #     return redirect(url_for('register'))
        address = request.form['address']
        payment_method = request.form['payment_method']
        payment_details = request.form['payment_details']

        new_user = User(username, password, email , address, payment_method, payment_details)
        save_user(new_user)
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifier = request.form['identifier']
        password = request.form['password']  
        user = retrieve_user(identifier)

        if user and user.password == password:
            session['username'] = user.username
            return redirect(url_for('show_cart'))
        else:
            pass
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/check-email', methods=['POST'])
def check_email():
    email = request.json['email']
    if retrieve_user(email):
        return jsonify({"exists": True})
    return jsonify({"exists": False})


######################################################





