from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail  # Import Flask-Mail

# Initialize the Flask application
app = Flask(__name__)
app.config.from_object('config')

# Initialize the database and migration tools
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Initialize Flask-Mail
mail = Mail(app)  # Add this line to initialize Flask-Mail with the app

from app import views, models