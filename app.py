import secrets
from flask import Flask
from myapp.product import init_product_routes
from myapp.user import init_user_routes

# Initialize the Flask application
app = Flask("Online Store")

# Generate a random secret key for the session
app.secret_key = secrets.token_hex(16)


init_product_routes(app)
init_user_routes(app)
