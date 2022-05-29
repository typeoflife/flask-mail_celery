from celery import Celery
from flask import jsonify, request
from jsonschema import validate, ValidationError
from app import app, db, mail
from models import User, Adv
from schema import USER_CREATE, ADV_CREATE
from flask_mail import Message
from generator import chunk_generator

celery = Celery('run', backend=app.config['result_backend'], broker=app.config['broker_url'])
celery.conf.update(app.config)


class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)


celery.Task = ContextTask


@celery.task()
def send_async_email(email_data):
    """Отправка email в фоновом режиме с Flask-Mail."""
    msg = Message(email_data['subject'],
                  sender=app.config['MAIL_DEFAULT_SENDER'],
                  recipients=(email_data['to']))
    msg.body = email_data['body']
    with app.app_context():
        mail.send(msg)


@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        response = jsonify({'status': 'User not found'})
        response.status_code = 404
        return response
    return jsonify({
        'id': user.id,
        'username': user.username
    })


@app.route('/user/', methods=['POST'])
def create_user():
    user_data = request.json
    try:
        validate(request.json, USER_CREATE)
    except ValidationError as er:
        response = jsonify({'success': False, 'error': er.message})
        response.status_code = 400
        return response
    if User.query.filter_by(username=user_data['username']).first() or User.query.filter_by(
            email=user_data['email']).first():
        response = jsonify({'status': 'Username or email is exists'})
        response.status_code = 400
        return response
    new_user = User(**user_data)
    new_user.set_password(request.json['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({
        'id': new_user.id
    })


@app.route('/adv/<int:adv_id>', methods=['GET'])
def get_adv(adv_id):
    adv = Adv.query.get(adv_id)
    if not adv:
        response = jsonify({'status': 'Advertisement  not found'})
        response.status_code = 404
        return response
    return jsonify({
        'id': adv.id
    })


@app.route('/adv/', methods=['POST'])
def create_adv():
    adv_data = request.json
    try:
        validate(request.json, ADV_CREATE)
    except ValidationError as er:
        response = jsonify({'success': False, 'error': er.message})
        response.status_code = 400
        return response
    if not User.query.get(adv_data['user_id']):
        response = jsonify({'status': 'User  not found'})
        response.status_code = 400
        return response
    new_adv = Adv(**adv_data)
    db.session.add(new_adv)
    db.session.commit()
    return jsonify({
        'id': new_adv.id
    })


@app.route('/adv/<int:adv_id>', methods=['DELETE'])
def delete_adv(adv_id):
    adv = Adv.query.get(adv_id)
    if not adv:
        response = jsonify({'status': 'Advertisement not found'})
        response.status_code = 404
        return response
    db.session.delete(adv)
    db.session.commit()
    return jsonify({
        'id': adv.id
    })


# Создаем список всех emails
def get_users_mails():
    users = User.query.all()
    mail_list = [user.email for user in users]
    return mail_list


# Отправляем всем пользователям email
@app.route('/send_emails', methods=['GET', 'POST'])
def send_emails():
    gen = chunk_generator(get_users_mails())
    for mails in gen:
        print(mails)
        email_data = {
            'subject': 'Hello from Flask!',
            'to': mails,
            'body': 'This is a test email sent from a background Celery task.'
        }

        send_async_email.delay(email_data)
    return {"status": 'success'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
