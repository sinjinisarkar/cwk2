from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer
from datetime import datetime


class Saree(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    category = db.Column(db.String(50), nullable=False)
    product_type = db.Column(db.String(50), nullable=False)  
    image_url = db.Column(db.String(200))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)  # Add this column

    def _repr_(self):
        return f"<Saree {self.name}>"
    
class CartItem(db.Model):
    __tablename__ = 'cart_item'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    saree_id = db.Column(db.Integer, db.ForeignKey('saree.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)

    # Relationships
    user = db.relationship('User', backref=db.backref('cart_items', lazy=True))
    saree = db.relationship('Saree', backref=db.backref('cart_items', lazy=True))
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    address = db.Column(db.String(255), nullable=True)

    def set_password(self, password):
        """Hash the password for secure storage."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify the password against the stored hash."""
        return check_password_hash(self.password_hash, password)
    
    def generate_reset_password_token(self, secret_key, expires_in=600):
        """Generate a token with a unique salt using the user's password hash."""
        serializer = URLSafeTimedSerializer(secret_key)
        return serializer.dumps(
            {'email': self.email},
            salt=self.password_hash  # Use the password hash as the salt
        )

    @staticmethod
    def validate_reset_password_token(token, secret_key, user_id):
        """Validate the token and return the user if valid."""
        serializer = URLSafeTimedSerializer(secret_key)
        user = User.query.get(user_id)
        if not user:
            return None
        try:
            data = serializer.loads(
                token,
                salt=user.password_hash,  # Validate using the current password hash
                max_age=600  # Token expiration in seconds
            )
        except Exception as ex:
            print(f"Token validation failed: {ex}")
            return None
        return user if data.get('email') == user.email else None


    def __repr__(self):
        return f'<User {self.email}>'


# many-to-many relationship between users and sarees in the wishlist
class WishlistItem(db.Model):
    __tablename__ = 'wishlist_item'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    saree_id = db.Column(db.Integer, db.ForeignKey('saree.id'), nullable=False)

    # Relationships
    user = db.relationship('User', backref=db.backref('wishlist_items', lazy=True))
    saree = db.relationship('Saree', backref=db.backref('wishlist_items', lazy=True))


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Nullable for guest users
    guest_info = db.Column(db.JSON, nullable=True)  # Store guest information as JSON
    total_price = db.Column(db.Float, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = db.relationship('User', backref=db.backref('orders', lazy=True))


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    saree_id = db.Column(db.Integer, db.ForeignKey('saree.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    # Relationships
    order = db.relationship('Order', backref=db.backref('order_items', lazy=True))
    saree = db.relationship('Saree')


