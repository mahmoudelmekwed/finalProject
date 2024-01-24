from flask import session , redirect , url_for , render_template , request
from myapp.models import User
from myapp.utilities import save_user, retrieve_user, username_exists, email_exists , save_products


def init_user_routes(app):

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
