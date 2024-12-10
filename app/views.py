from flask import render_template, flash, redirect, url_for, request, session, g, json, current_app
from app import app, db, mail
from app.models import Saree, User, CartItem, WishlistItem, Order, OrderItem
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from datetime import datetime, timedelta



@app.route('/')
def index():
    sarees = Saree.query.all()

    # Fetch sarees added in the last 30 days
    cutoff_date = datetime.utcnow() - timedelta(days=30)
    new_arrivals = Saree.query.filter(Saree.date_added >= cutoff_date).order_by(Saree.date_added.desc()).limit(4).all()
    print(f"New Arrivals: {new_arrivals}")  # Debug output

    return render_template('index.html', sarees=sarees, new_arrivals=new_arrivals)

@app.route('/categories', defaults={'category_name': None, 'product_type': None})
@app.route('/categories/<string:product_type>/<string:category_name>')
@app.route('/categories/<string:product_type>', defaults={'category_name': None})
def categories(product_type, category_name):
    # Check if product_type is provided (sarees, lehengas, etc.)
    if product_type:
        products = Saree.query.filter_by(product_type=product_type).all()

        # If category_name is provided, filter further
        if category_name:
            products = [saree for saree in products if saree.category == category_name]

            if not products:
                flash(f"No {product_type} found for {category_name}.", "warning")
                return redirect(url_for('categories', product_type=product_type))

        category_name = category_name or "All"

    else:
        # If no product_type, show all products (fallback behavior)
        products = Saree.query.all()
        category_name = "All"
    
    # Construct breadcrumbs
    breadcrumbs = []
    if product_type:
        breadcrumbs.append({
            "name": product_type.capitalize(),
            "url": url_for('categories', product_type=product_type)
        })
        if category_name and category_name != "All":
            breadcrumbs.append({"name": category_name.capitalize(), "url": ""})  # No URL for the last crumb


    return render_template(
        'categories.html',
        sarees=products,
        category_name=category_name,
        product_type=product_type,
        breadcrumbs=breadcrumbs
    )



@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        # Log in the user
        session['user_id'] = user.id
        flash("Login successful!", "success")

        # Retrieve user's existing cart from the database
        user_cart_items = CartItem.query.filter_by(user_id=user.id).all()
        user_cart = {item.saree_id: item.quantity for item in user_cart_items}

        # Get the guest cart from the session
        guest_cart = session.get('cart', [])

        # Merge guest cart into user's cart
        for guest_item in guest_cart:
            saree_id = guest_item['id']
            quantity = guest_item['quantity']
            if saree_id in user_cart:
                user_cart[saree_id] += quantity  # Add quantities
            else:
                user_cart[saree_id] = quantity  # Add new item

        # Save the merged cart back to the database
        for saree_id, quantity in user_cart.items():
            existing_item = CartItem.query.filter_by(user_id=user.id, saree_id=saree_id).first()
            if existing_item:
                existing_item.quantity = quantity
            else:
                new_item = CartItem(user_id=user.id, saree_id=saree_id, quantity=quantity)
                db.session.add(new_item)

        db.session.commit()

        # Clear the guest cart from the session
        session.pop('cart', None)

        return redirect(url_for('index'))
    else:
        flash("Invalid credentials!", "danger")
        return redirect(url_for('index'))


@app.before_request
def load_logged_in_user():
    """Load the currently logged-in user."""
    user_id = session.get('user_id')
    if user_id:
        g.current_user = User.query.get(user_id)
    else:
        g.current_user = None


@app.route('/logout')
def logout():
    """Log out the user by clearing the session."""
    session.pop('user_id', None)  # Remove user ID from the session
    session.pop('cart', None)     # Clear the guest cart from the session
    flash("You have successfully logged out.", "info")
    return redirect(url_for('index'))



@app.route('/signup', methods=['POST'])
def signup():
    email = request.form.get('email')
    password = request.form.get('password')

    if User.query.filter_by(email=email).first():
        flash("Email already registered!", "danger")
        return redirect(url_for('index'))

    new_user = User(email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    flash("Signup successful! Please log in to your account.", "success")
    return redirect(url_for('index'))

@app.route('/checkout-options', methods=['GET', 'POST'])
def checkout_options():
    if request.method == 'POST':
        # Handle guest checkout form submission
        guest_name = request.form.get('name')
        guest_email = request.form.get('email')
        shipping_address = request.form.get('address')

        # Store guest details in the session
        session['guest_info'] = {
            'name': guest_name,
            'email': guest_email,
            'address': shipping_address,
        }

        flash("Guest details saved. Proceeding to checkout.", "success")
        return redirect(url_for('checkout'))  # Redirect to the checkout route

    return render_template('checkout_options.html')  # Render the options page




@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    print("Checkout route executed.")
    if session.get('user_id'):
        user_id = session.get('user_id')
        cart_items = CartItem.query.filter_by(user_id=user_id).all()
        guest_info = None
    else:
        guest_info = session.get('guest_info')
        if not guest_info:
            flash("Please complete the guest checkout first.", "danger")
            return redirect(url_for('checkout_options'))
        cart_items = session.get('cart', [])
        user_id = None

    if request.method == 'POST':
        total_price = 0
        for item in cart_items:
            if user_id:
                saree = Saree.query.get(item.saree_id)
                quantity = item.quantity
            else:
                saree = Saree.query.get(item['id'])
                quantity = item['quantity']

            if saree.stock >= quantity:
                saree.stock -= quantity
                total_price += saree.price * quantity
            else:
                flash(f"Not enough stock for {saree.name}.", "danger")
                return redirect(url_for('view_cart'))

        print(f"Total price for order: {total_price}")

        new_order = Order(
            user_id=user_id,
            guest_info=guest_info,
            total_price=total_price
        )
        db.session.add(new_order)
        db.session.commit()
        print(f"Order created: {new_order.id}")

        for item in cart_items:
            if user_id:
                saree = Saree.query.get(item.saree_id)
                quantity = item.quantity
            else:
                saree = Saree.query.get(item['id'])
                quantity = item['quantity']

            order_item = OrderItem(
                order_id=new_order.id,
                saree_id=saree.id,
                quantity=quantity,
                price=saree.price
            )
            db.session.add(order_item)
            print(f"OrderItem created: {order_item}")

        if user_id:
            CartItem.query.filter_by(user_id=user_id).delete()
        else:
            session.pop('cart', None)
            session.pop('guest_info', None)

        db.session.commit()
        print("Order and OrderItems committed successfully.")
        flash("Checkout complete!", "success")
        return redirect(url_for('categories'))

    return render_template('address.html', user=session.get('user_id'), guest_info=session.get('guest_info'))





@app.route('/guest-checkout', methods=['GET', 'POST'])
def guest_checkout():
    if request.method == 'POST':
        guest_name = request.form.get('name')
        guest_email = request.form.get('email')
        shipping_address = request.form.get('address')

        # Store guest details in the session
        session['guest_info'] = {
            'name': guest_name,
            'email': guest_email,
            'address': shipping_address,
        }

        flash("Guest details saved. Proceeding to checkout.", "success")
        return redirect(url_for('payment'))

    return render_template('guest_checkout.html')



@app.before_request
def initialize_cart():
    """Ensure that the cart exists in the session."""
    if 'cart' not in session:
        session['cart'] = []


@app.route('/add-to-cart/<int:saree_id>', methods=['POST'])
def add_to_cart(saree_id):
    """Add a saree to the cart."""
    saree = Saree.query.get_or_404(saree_id)  # Fetch the saree from the database
    user_id = session.get('user_id')
    quantity = int(request.form.get('quantity', 1))  # Get quantity from form, default to 1

    if user_id:
        # Logged-in user: use CartItem model
        existing_item = CartItem.query.filter_by(user_id=user_id, saree_id=saree_id).first()

        if existing_item:
            # If the item already exists in the user's cart, increment the quantity
            existing_item.quantity += quantity
        else:
            # Otherwise, add the item to the user's cart
            new_cart_item = CartItem(user_id=user_id, saree_id=saree_id, quantity=quantity)
            db.session.add(new_cart_item)

        db.session.commit()  # Commit changes to the database
    else:
        # Guest user: use session-based cart
        cart = session.get('cart', [])

        for item in cart:
            if item['id'] == saree.id:
                item['quantity'] += quantity
                item['subtotal'] = item['price'] * item['quantity']  # Update subtotal
                break
        else:
            cart.append({
                'id': saree.id,
                'name': saree.name,
                'price': saree.price,
                'image': saree.image_url,
                'quantity': quantity,
                'subtotal': saree.price * quantity
            })

        session['cart'] = cart
        session.modified = True  # Mark session as updated

    flash(f"{quantity} x {saree.name} added to cart!", "success")
    return redirect(request.referrer or url_for('categories'))  # Redirect back to the previous page

@app.route('/remove-from-cart/<int:saree_id>')
def remove_from_cart(saree_id):
    """Remove a saree from the cart."""
    user_id = session.get('user_id')  # Check if the user is logged in
    if user_id:  # For logged-in users
        # Remove the item from the database cart
        cart_item = CartItem.query.filter_by(user_id=user_id, saree_id=saree_id).first()
        if cart_item:
            db.session.delete(cart_item)
            db.session.commit()
    else:  # For guest users
        # Remove the item from the session-based cart
        cart = session.get('cart', [])
        cart = [item for item in cart if item['id'] != saree_id]
        session['cart'] = cart
        session.modified = True

    flash("Item removed from cart.", "info")
    return redirect(url_for('view_cart'))



@app.before_request
def load_cart():
    """Load the cart into the global context for use in the cart modal."""
    g.cart_total = 0
    g.cart = []  # Default empty cart

    if 'user_id' in session:
        # Logged-in user: fetch cart from the database
        user_id = session['user_id']
        db_cart_items = CartItem.query.filter_by(user_id=user_id).all()
        g.cart = [
            {
                'id': item.saree.id,
                'name': item.saree.name,
                'price': item.saree.price,
                'quantity': item.quantity,
                'subtotal': item.saree.price * item.quantity,
                'image': item.saree.image_url
            }
            for item in db_cart_items
        ]
        g.cart_total = sum(item['subtotal'] for item in g.cart)
    else:
        # Guest user: fetch cart from session
        g.cart = session.get('cart', [])
        g.cart_total = sum(item['price'] * item['quantity'] for item in g.cart)



@app.route('/view-cart')
def view_cart():
    if 'user_id' in session:  # Logged-in user
        user_id = session['user_id']
        db_cart_items = CartItem.query.filter_by(user_id=user_id).all()

        cart = []
        for item in db_cart_items:
            saree = Saree.query.get(item.saree_id)
            if saree.stock < item.quantity:
                flash(f"Stock for {saree.name} has changed. Available stock: {saree.stock}.", "warning")
                item.quantity = min(item.quantity, saree.stock)  # Adjust cart quantity to available stock
                db.session.commit()

            cart.append({
                'id': saree.id,
                'name': saree.name,
                'price': saree.price,
                'quantity': item.quantity,
                'subtotal': saree.price * item.quantity,
                'image': saree.image_url
            })
        total_price = sum(item['subtotal'] for item in cart)
    else:
        cart = session.get('cart', [])
        for item in cart:
            saree = Saree.query.get(item['id'])
            if saree.stock < item['quantity']:
                flash(f"Stock for {saree.name} has changed. Available stock: {saree.stock}.", "warning")
                item['quantity'] = min(item['quantity'], saree.stock)  # Adjust cart quantity to available stock
            item['subtotal'] = item['price'] * item['quantity']
        session['cart'] = cart
        session.modified = True
        total_price = sum(item['subtotal'] for item in cart)

    return render_template('view_cart.html', cart=cart, total_price=total_price)


def merge_cart(user_id):
    """Merge the guest cart with the logged-in user's cart."""
    guest_cart = session.get('cart', [])
    user_cart_key = f'cart_{user_id}'
    user_cart = session.get(user_cart_key, [])

    for guest_item in guest_cart:
        for user_item in user_cart:
            if user_item['id'] == guest_item['id']:
                user_item['quantity'] += guest_item['quantity']
                break
        else:
            user_cart.append(guest_item)

    # Save the merged cart
    session[user_cart_key] = user_cart
    session.pop('cart', None)  # Clear the guest cart
    session.modified = True

@app.route('/update-quantity', methods=['POST'])
def update_quantity():
    data = json.loads(request.data)  # Parse JSON from the request
    item_id = int(data.get('item_id'))  # Get the item ID
    action = data.get('action')  # Get the action (increment or decrement)

    if 'user_id' in session:
        # Logged-in user: update quantity in the database
        user_id = session['user_id']
        cart_item = CartItem.query.filter_by(user_id=user_id, saree_id=item_id).first()

        if not cart_item:
            return json.dumps({'status': 'error', 'message': 'Item not found'}), 404

        if action == 'increment':
            cart_item.quantity += 1
        elif action == 'decrement':
            cart_item.quantity = max(1, cart_item.quantity - 1)  # Ensure quantity is at least 1

        db.session.commit()

        # Recalculate cart total
        cart_items = CartItem.query.filter_by(user_id=user_id).all()
        item_subtotal = cart_item.saree.price * cart_item.quantity
        total_price = sum(item.saree.price * item.quantity for item in cart_items)

        return json.dumps({'status': 'OK', 'new_quantity': cart_item.quantity, 'new_subtotal': item_subtotal, 'new_total': total_price})
    else:
        # Guest user: update quantity in session cart
        cart = session.get('cart', [])
        for item in cart:
            if item['id'] == item_id:
                if action == 'increment':
                    item['quantity'] += 1
                elif action == 'decrement':
                    item['quantity'] = max(1, item['quantity'] - 1)  # Ensure quantity is at least 1
                    item['subtotal'] = item['price'] * item['quantity']  # Update subtotal
                # Update the subtotal
                item['subtotal'] = item['price'] * item['quantity']
                break
        else:
            return json.dumps({'status': 'error', 'message': 'Item not found'}), 404

        session['cart'] = cart
        session.modified = True

        # Recalculate cart total
        total_price = sum(item['subtotal'] for item in cart)

        return json.dumps({'status': 'OK', 'new_quantity': item['quantity'], 'new_subtotal': item['subtotal'], 'new_total': total_price})



@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()

        if user:
            token = user.generate_reset_password_token(
                secret_key=app.config['SECRET_KEY']
            )
            # Create the password reset URL
            reset_url = url_for('reset_password', token=token, user_id=user.id, _external=True)
            # Send the reset email directly in this view
            subject = 'Password Reset Request'
            msg = Message(
                subject,
                recipients=[email],
                body=f"""To reset your password, visit the following link: {reset_url}\n
If you did not make this request, please ignore this email. This link expires in 10 minutes"""
            )
            mail.send(msg)

            flash('A password reset link has been sent to your email.', 'info')
        else:
            flash('No account found with that email address.', 'danger')

        return redirect(url_for('forgot_password'))

    return render_template('forgot_password.html')



@app.route('/reset-password/<token>/<int:user_id>', methods=['GET', 'POST'])
def reset_password(token, user_id):
    user = User.validate_reset_password_token(
        token, secret_key=app.config['SECRET_KEY'], user_id=user_id
    )
    if not user:
        flash('Invalid or expired reset link!', 'danger')
        return redirect(url_for('forgot_password'))

    if request.method == 'POST':
        new_password = request.form.get('password')
        if new_password:
            user.set_password(new_password)
            db.session.commit()
            flash('Your password has been updated! You can now log in.', 'success')
            return redirect(url_for('index'))
    return render_template('reset_password.html')


@app.route('/payment', methods=['GET', 'POST'])
def payment():
    # Check if user is logged in
    if session.get('user_id'):  
        user_id = session.get('user_id')
        cart_items = CartItem.query.filter_by(user_id=user_id).all()
        guest_info = None
    else:
        # Check for guest info in session
        guest_info = session.get('guest_info')
        if not guest_info:
            flash("Please complete the guest checkout first.", "danger")
            return redirect(url_for('checkout_options'))
        cart_items = session.get('cart', [])
        user_id = None

    if request.method == 'POST':
        total_price = 0

        # Process each cart item and calculate total price
        for item in cart_items:
            if user_id:  # Logged-in user
                saree = Saree.query.get(item.saree_id)
                quantity = item.quantity
            else:  # Guest user
                saree = Saree.query.get(item['id'])
                quantity = item['quantity']

            # Check stock availability
            if saree.stock >= quantity:
                saree.stock -= quantity  # Reduce stock
                total_price += saree.price * quantity  # Calculate total price
            else:
                flash(f"Not enough stock for {saree.name}. Available: {saree.stock}.", "danger")
                return redirect(url_for('view_cart'))

        # Create a new order
        new_order = Order(
            user_id=user_id,
            guest_info=guest_info,
            total_price=total_price
        )
        db.session.add(new_order)
        db.session.commit()  # Save the order to get its ID
        print(f"Order created: {new_order.id}")

        # Add order items
        for item in cart_items:
            if user_id:  # Logged-in user
                saree = Saree.query.get(item.saree_id)
                quantity = item.quantity
            else:  # Guest user
                saree = Saree.query.get(item['id'])
                quantity = item['quantity']

            order_item = OrderItem(
                order_id=new_order.id,
                saree_id=saree.id,
                quantity=quantity,
                price=saree.price
            )
            db.session.add(order_item)

        # Clear the cart after checkout
        if user_id:  # Logged-in user
            CartItem.query.filter_by(user_id=user_id).delete()
        else:  # Guest user
            session.pop('cart', None)  # Clear guest cart
            session.pop('guest_info', None)  # Clear guest info

        db.session.commit()  # Commit all changes to the database
        flash("Payment successful! Thank you for your purchase.", "success")
        return redirect(url_for('index'))

    return render_template(
        'payment.html',
        user=g.current_user if session.get('user_id') else None,
        guest_info=session.get('guest_info'),
    )


@app.route('/saree/<int:saree_id>', methods=['GET', 'POST'])
def saree_detail(saree_id):
    saree = Saree.query.get_or_404(saree_id)

    # Construct breadcrumbs
    breadcrumbs = [
        {"name": saree.product_type.capitalize(), "url": url_for('categories', product_type=saree.product_type)},
        {"name": saree.category.capitalize(), "url": url_for('categories', product_type=saree.product_type, category_name=saree.category)},
        {"name": saree.name, "url": ""}
    ]

    if request.method == 'POST':
        quantity = int(request.form.get('quantity', 1))

        if 'user_id' in session:
            user_id = session['user_id']
            cart_item = CartItem.query.filter_by(user_id=user_id, saree_id=saree.id).first()
            if cart_item:
                cart_item.quantity += quantity
            else:
                new_cart_item = CartItem(user_id=user_id, saree_id=saree.id, quantity=quantity)
                db.session.add(new_cart_item)
            db.session.commit()
        else:
            cart = session.get('cart', [])
            for item in cart:
                if item['id'] == saree.id:
                    item['quantity'] += quantity
                    break
            else:
                cart.append({
                    'id': saree.id,
                    'name': saree.name,
                    'price': saree.price,
                    'quantity': quantity,
                    'image': saree.image_url,
                })
            session['cart'] = cart
            session.modified = True

        flash(f"{quantity} x {saree.name} added to your cart.", "success")
        return redirect(url_for('saree_detail', saree_id=saree.id))

    return render_template('saree_detail.html', saree=saree, breadcrumbs=breadcrumbs)



@app.route('/add-to-wishlist/<int:saree_id>', methods=['POST'])
def add_to_wishlist(saree_id):
    """Add a saree to the wishlist."""
    # Check if the user is logged in
    if 'user_id' not in session:
        flash("Please log in to add items to your wishlist.", "warning")
        return redirect(url_for('index'))  # Redirect to login page or index

    saree = Saree.query.get_or_404(saree_id)  # Fetch the saree from the database
    user_id = session['user_id']

    # Check if the saree is already in the user's wishlist
    existing_item = WishlistItem.query.filter_by(user_id=user_id, saree_id=saree_id).first()
    if existing_item:
        flash(f"{saree.name} is already in your wishlist!", "info")
        return redirect(url_for('wishlist'))

    # Add the saree to the wishlist
    new_wishlist_item = WishlistItem(user_id=user_id, saree_id=saree_id)
    db.session.add(new_wishlist_item)
    db.session.commit()

    flash(f"{saree.name} added to wishlist!", "success")
    return redirect(url_for('wishlist'))


@app.route('/wishlist')
def wishlist():
    """Show all items in the wishlist."""
    if 'user_id' not in session:
        flash("Please log in to view your wishlist.", "warning")
        return redirect(url_for('index'))  # Redirect to login page or index

    user_id = session['user_id']
    wishlist_items = WishlistItem.query.filter_by(user_id=user_id).all()

    wishlist = [
        {
            'id': item.saree.id,
            'name': item.saree.name,
            'price': item.saree.price,
            'image': item.saree.image_url
        }
        for item in wishlist_items
    ]

    return render_template('wishlist.html', wishlist=wishlist)

@app.route('/remove-from-wishlist/<int:saree_id>', methods=['POST'])
def remove_from_wishlist(saree_id):
    """Remove an item from the wishlist."""
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in to manage your wishlist.", "danger")
        return redirect(url_for('login'))

    # Remove from the WishlistItem model
    wishlist_item = WishlistItem.query.filter_by(user_id=user_id, saree_id=saree_id).first()
    if wishlist_item:
        db.session.delete(wishlist_item)
        db.session.commit()

    flash("Item removed from wishlist.", "info")
    return redirect(url_for('wishlist'))


@app.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy_policy.html')


@app.route('/profile')
def profile():
    # Ensure the user is logged in
    if 'user_id' not in session:
        flash("Please log in to access your profile.", "warning")
        return redirect(url_for('login'))

    # Fetch user details
    user = User.query.get(session['user_id'])

    # Fetch user's orders
    orders = Order.query.filter_by(user_id=user.id).order_by(Order.date_created.desc()).all()

    # Fetch user's wishlist items (if implemented)
    wishlist_items = WishlistItem.query.filter_by(user_id=user.id).all()

    # Render the profile page with the fetched data
    return render_template(
        'profile.html',
        user=user,
        orders=orders,
        wishlist_items=wishlist_items
    )

@app.route('/order/<int:order_id>')
def order_details(order_id):
    # Fetch the order by its ID
    order = Order.query.get_or_404(order_id)

    # If the user is logged in, verify that the order belongs to them
    if 'user_id' in session and order.user_id != session['user_id']:
        flash("You are not authorized to view this order.", "danger")
        return redirect(url_for('profile'))

    # If guest, verify that the guest info matches
    if 'guest_info' in session and order.guest_info != session['guest_info']:
        flash("You are not authorized to view this order.", "danger")
        return redirect(url_for('profile'))

    return render_template('order_details.html', order=order)



@app.route('/search')
def search():
    query = request.args.get('q', '').strip()  # Get the search term and strip whitespace
    if not query:
        flash("Please enter a search term.", "warning")
        return redirect(url_for('index'))
    
    # Search for sarees by name or description
    results = Saree.query.filter(
        (Saree.name.ilike(f"%{query}%")) | (Saree.description.ilike(f"%{query}%"))
    ).all()
    
    return render_template('search_results.html', query=query, results=results)



@app.route('/address', methods=['GET', 'POST'])
def address():
    if 'user_id' not in session:
        flash("Please log in to access this page.", "danger")
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Debug: Print form data
        print(request.form)

        user = User.query.get(session['user_id'])

        # Save the shipping address
        user.address = request.form.get('address')
        db.session.commit()

        flash("Address saved successfully! Redirecting to payment...", "success")
        return redirect(url_for('payment'))

    return render_template('address.html')

