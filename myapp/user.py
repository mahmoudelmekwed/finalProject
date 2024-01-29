from flask import session , redirect , url_for , render_template , request
from myapp.models import User
from myapp.utilities import save_user, retrieve_user, username_exists, email_exists , save_products , is_valid_name , is_valid_address , is_valid_telephone , is_valid_card_number , is_valid_expiry_date , is_valid_cvc


def init_user_routes(app):

    # Flask route to handle the checkout process
    @app.route('/checkout' , methods=['GET', 'POST'])
    def checkout():
        if 'username' not in session:
            return redirect(url_for('login'))
        
        user = retrieve_user(session['username'])

        if not user:
            return redirect(url_for('login'))

        total_price = session.get('total_price', 0)
        total_quantity = session.get('total_quantity', 0)
        return render_template('checkout.html', errors={}, total_price=total_price, total_quantity=total_quantity)
    

    @app.route('/validate_checkout', methods=['POST'])
    def validate_checkout():

        
        # Extract from data
        name = request.form.get('name' , '')
        address = request.form.get('address' , '')
        telephone = request.form.get('telephone' , '')
        card_number = request.form.get('card_number' , '')
        expiry_date = request.form.get('expiry_date' , '')
        cvc = request.form.get('cvc' , '')

        # Perform validations
        errors = {}
        if not is_valid_name(name):
            errors['name'] = "Invalid name"
        if not is_valid_address(address):
            errors['address'] = "Invalid address"
        if not is_valid_telephone(telephone):
            errors['telephone'] = "Invalid telephone"
        if not is_valid_card_number(card_number):
            errors['card_number'] = "Invalid card number"
        if not is_valid_expiry_date(expiry_date):
            errors['expiry_date'] = "Invalid expiry date"
        if not is_valid_cvc(cvc):
            errors['cvc'] = "Invalid cvc" 

        
        if errors:
        # If there are errors, redirect back to checkout page with errors
            print(errors)
            return render_template('checkout.html', errors=errors)

        # If validation passes, you can proceed with the checkout process
        # For example, redirect to a confirmation route or handle the process here
        return redirect(url_for('confirmation'))


    # Flask route for order confirmation
    @app.route('/confirmation', methods=['GET'])
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
    

