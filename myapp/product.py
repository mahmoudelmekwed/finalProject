import json
from flask import session , redirect , url_for , render_template , request
from myapp.utilities import retrieve_user, save_products , load_products

def init_product_routes(app):

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
                    'unit_price': product.price, 
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