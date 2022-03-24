from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
import config


app = Flask('app')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_mapping(SQLALCHEMY_DATABASE_URI=config.SQLALCHEMY_DATABASE_URI)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/3'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/4'
db = SQLAlchemy(app)

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.mail.ru'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = '***'
app.config['MAIL_PASSWORD'] = '***'
app.config['MAIL_DEFAULT_SENDER'] = '***'

mail = Mail(app)
