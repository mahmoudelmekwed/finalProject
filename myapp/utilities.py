import json , re
from myapp.models import Product , User

def load_users():
    with open('users.json', 'r') as file:
        return json.load(file)

# Load products from a JSON file
def load_products(filename):
    with open(filename, 'r') as file:
            products_data = json.load(file)
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

# Validation functions for checkout page
def is_valid_name(name):
    return len(name) > 0 and len(name) < 100 and all(char.isalpha() or char.isspace() for char in name)

def is_valid_address(address):
    return len(address) > 0

def is_valid_telephone(telephone):
    return bool(re.match(r'^[+\d\s-]{7,15}$', telephone))

def is_valid_card_number(card_number):
    print(f"Validating card number: {card_number}")
    return bool(re.match(r'^\d{13,19}$', card_number))

def is_valid_expiry_date(expiry_date):
    print(f"Validating expiry date: {expiry_date}")
    return bool(re.match(r'^\d{2}/\d{2}$', expiry_date))

def is_valid_cvc(cvc):
    print(f"Validating cvc: {cvc}")
    return bool(re.match(r'^\d{3}$', cvc))