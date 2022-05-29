from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
import config

#Flask & db
app = Flask('app')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_mapping(SQLALCHEMY_DATABASE_URI=config.SQLALCHEMY_DATABASE_URI)
db = SQLAlchemy(app)

# Celery configuration
app.config['result_backend'] = 'redis://localhost:6379/1'
app.config['broker_url'] = 'redis://localhost:6379/2'


# Flask-Mail configuration
app.config['MAIL_SERVER']='smtp.mail.ru'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = '***'
app.config['MAIL_PASSWORD'] = '***'
app.config['MAIL_DEFAULT_SENDER'] = '***'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)
