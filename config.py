import os

# Set the base directory of the project
basedir = os.path.abspath(os.path.dirname(__file__))

# Database configuration
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'sarees.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Application settings
SECRET_KEY = 'a3f4b8c1d2e6f9g7h8i1j2k3l4m5n6o7'  # Replace with a newly generated key for production
SECURITY_PASSWORD_SALT = 'your-secret-salt'

# Flask-WTF settings
WTF_CSRF_ENABLED = True

# Email Configuration
MAIL_SERVER = 'smtp.gmail.com'  # Use your email provider's SMTP server
MAIL_PORT = 587  # Usually 587 for TLS
MAIL_USE_TLS = True  # Use TLS encryption
MAIL_USE_SSL = False  # Usually False if TLS is True
MAIL_USERNAME = 'no.reply.nakshikantha@gmail.com'  # Replace with your email
MAIL_PASSWORD = 'mhlk jvlt utlj fija'  # Replace with your email password or app password
MAIL_DEFAULT_SENDER = 'no.reply.nakshikantha@gmail.com'  # Default sender email address for outgoing emails

