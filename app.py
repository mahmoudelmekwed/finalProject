import json
import secrets
from flask import Flask, render_template , request, session , url_for ,redirect

# Initialize the Flask application
app = Flask("Online Store")
# Generate a random secret key for the session
app.secret_key = secrets.token_hex(16)

# Define the Product class to represent each product in the store
class Product:
    def __init__(self, id, image, name, price, description, quantity):
        self.id = id
        self.image = image
        self.name = name
        self.price = price
        self.description = description
        self.quantity = quantity

    # Calculate the total price of the product based on its quantity
    def total_price(self):
        return round(self.price * self.quantity, 2)

# Define the User class to represent each user of the store
class User:
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        # Load user's cart from a JSON file
        self.cart = self.load_user_cart()

    # Load the user's cart from a file or initialize an empty cart
    def load_user_cart(self):
        try:
            with open('cart.json', 'r') as file:
                cart = json.load(file)
            return cart.get(self.username, {"items": []})
        except FileNotFoundError:
            return {"items": []}

    # Calculate the total price of all items in the cart
    def calculate_cart_total(self):
        total = 0
        for item in self.cart['items']:
            total += item['price']
        return round(total, 2)

    # Calculate the total quantity of all items in the cart
    def calculate_cart_quantity(self):
        total_quantity = 0
        for item in self.cart['items']:
            total_quantity += item['quantity']
        return total_quantity

    # Clear the user's cart
    def clear_cart(self):
        self.cart['items'] = []

# Load products from a JSON file
def load_products(filename):
    file = open(filename, 'r')
    products_data = json.load(file)
    file.close()
    products = []
    for p in products_data:
        product = Product(p['id'], p['image'], p['name'], p['price'], p['description'], p['quantity'])
        products.append(product)

    return products

# Save the cart data to a JSON file
def save_products(cart):
    file = open('cart.json', 'w')
    json.dump(cart, file)
    file.close()

# Flask route for the homepage
@app.route("/")
def home():
    products = load_products("products.json")

    if 'username' in session:
        user = retrieve_user(session['username'])
        total_quantity = user.calculate_cart_quantity()
        session['total_quantity'] = total_quantity
    else:
        total_quantity = 0

    return render_template("index.html", products=products, total_quantity=total_quantity)

# Route to display the details of a specific product based on its product_id
@app.route('/product/<product_id>')
def product_detail(product_id):
    products = load_products("products.json")
    product = None
    for p in products:
        if str(p.id) == product_id:
            product = p
            break
    # Retrieve the total quantity of items in the user's session (shopping cart)
    total_quantity = session.get('total_quantity' , 0)
    if product:
        return render_template('product_detail.html', product=product , total_quantity=total_quantity)
    else:
        return "Product not found"
    
# Flask route to handle the search functionality
@app.route("/search")
def search_products():
    product_to_find = request.args.get("product_to_find")
    product_to_find = product_to_find.lower()
    products = load_products("products.json")
    filtered_products = []
    for p in products:
        if product_to_find in p.name.lower():
            filtered_products.append(p)

    total_quantity = session.get('total_quantity' , 0)
    
    return render_template("search.html" , products = filtered_products , product_to_find = product_to_find , total_quantity=total_quantity)

# Flask route to add products to the shopping cart
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

# Flask route to remove products from the shopping cart
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

# Flask route to display the user's shopping cart
@app.route('/cart')
def show_cart():
    if 'username' not in session:
        return redirect(url_for('login'))

    user = retrieve_user(session['username'])

    if not user:
        return redirect(url_for('login'))
    
    total_price = user.calculate_cart_total()
    total_quantity = user.calculate_cart_quantity()

    session['total_price'] = total_price
    session['total_quantity'] = total_quantity

    return render_template('cart.html', cart_items=user.cart['items'] , total_price = total_price , total_quantity = total_quantity)


# Flask route to handle the checkout process
@app.route('/checkout' , methods=['POST'])
def checkout():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    user = retrieve_user(session['username'])

    if not user:
        return redirect(url_for('login'))    
    
    total_price = session.get('total_price' , 0)
    total_quantity = session.get('total_quantity' , 0)
    return render_template('checkout.html' , total_price = total_price , total_quantity = total_quantity)


# Flask route for order confirmation
@app.route('/confirmation', methods=['POST'])
def confirmation():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    user = retrieve_user(session['username'])

    if not user:
        return redirect(url_for('login'))    
    
    total_price = session.get('total_price' , 0)

    session['total_quantity'] = 0
    user.clear_cart()
    save_products(user.cart)
    return render_template('confirmation.html' , total_price = total_price)

# Opens and reads the JSON file containing user data
def load_users():
    with open('users.json', 'r') as file:
        return json.load(file)

# Function to save user data to a JSON file
def save_user(user):
    try:
        users = load_users()
    except (FileNotFoundError, json.JSONDecodeError):
        users = []

    user_data = {
        'username': user.username,
        'password': user.password,
        'email' : user.email
    }

    users.append(user_data)

    with open('users.json', 'w') as file:
        json.dump(users, file)


# Function to retrieve a user from a JSON file
def retrieve_user(identifier):
    try:
        users = load_users()
        for user_data in users:
            if user_data['username'] == identifier or user_data['email'] == identifier:
                return User(
                    username=user_data['username'], 
                    password=user_data['password'],
                    email =user_data['email']
                )
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return None

#Checks if the given username exists in the user data.
def username_exists(username):
    users = load_users()
    for user in users:
        if user['username'] == username:
            return True
    return False

#Checks if the given email exists in the user data.
def email_exists(email):
    users = load_users()
    for user in users:
        if user['email'] == email:
            return True
    return False

# Flask route for user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    username_error = None
    email_error = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'] 
        email = request.form['email'] 

        if username_exists(username):
            username_error = 'Username is already in use.'

        if email_exists(email):
            email_error = 'Email is already in use.'

        if username_error or email_error:
            return render_template('register.html', username_error=username_error, email_error=email_error)

        new_user = User(username, password, email)
        save_user(new_user)
        return redirect(url_for('login'))
    return render_template('register.html')

# Flask route for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        identifier = request.form['identifier']
        password = request.form['password']  
        user = retrieve_user(identifier)

        if user is None:
            error = 'Username not found.'
        elif user.password != password:
            error = 'Incorrect password.'
        else:
            session['username'] = user.username
            return redirect(url_for('home'))

    return render_template('login.html' , error=error)

# Flask route for user logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))
