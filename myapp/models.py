import json

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