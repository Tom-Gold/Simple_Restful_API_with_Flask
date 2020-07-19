from flask import Flask, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
import os
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from models import *
# import db_init

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'company_api.db')
app.config['JWT_SECRET_KEY'] = 'jwt_key'
app.secret_key = 'secret_key'

db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)

# app.register_blueprint(models_bp)

#
# @app.cli.command('test')
# def test():
#     print('test')
#
# # Creates the database
# @app.cli.command('db_create')
# def db_create():
#     db.create_all()
#     print('Database created!')
#
# # Clears the database
# @app.cli.command('db_drop')
# def db_drop():
#     db.drop_all()
#     print('Database dropped!')
#
# # Seeding the database
# @app.cli.command('db_seed')
# def db_seed():
#     test_msg_1 = Msg(msg_subject='test_msg_1 subject',
#                      msg_content='test_msg_1 content',
#                      msg_creation_date='1/1/20')
#
#     test_msg_2 = Msg(msg_subject='test_msg_2 subject',
#                      msg_content='test_msg_2 content',
#                      msg_creation_date='1/1/20')
#
#     test_msg_3 = Msg(msg_subject='test_msg_3 subject',
#                      msg_content='test_msg_3 content',
#                      msg_creation_date='1/1/20')
#
#     db.session.add(test_msg_1)
#     db.session.add(test_msg_2)
#     db.session.add(test_msg_3)
#
#     test_user_sender = User(first_name='William',
#                             last_name='sender',
#                             email='test@test.com',
#                             password='P@ssw0rd')
#
#     test_user_receiver = User(first_name='William',
#                               last_name='receiver',
#                               email='test_rec@test.com',
#                               password='P@ssw0rd')
#     db.session.add(test_user_sender)
#     db.session.add(test_user_receiver)
#
#     db.session.flush()
#
#     test_transaction = Transaction(msg_from=test_user_sender.id,
#                                    msg_to=test_user_receiver.id,
#                                    msg_index=test_msg_1.id,
#                                    msg_read=0)
#
#     db.session.add(test_transaction)
#     db.session.commit()
#     print('Database seeded!')

@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    test = User.query.filter_by(email=email).first()
    if test:
        return jsonify(message='That email already exists.'), 409
    else:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        user = User(first_name=first_name, last_name=last_name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify(message="User created successfully."), 201


@app.route('/login', methods=['POST'])
def login():
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
    else:
        email = request.form['email']
        password = request.form['password']

    user = User.query.filter_by(email=email, password=password).first()
    if user:
        access_token = create_access_token(identity=email)
        session['user_id'] = user.id
        session['email'] = email
        return jsonify(message="Login succeeded!", access_token=access_token)
    else:
        return jsonify(message="Bad email or password"), 401

# Write message
@app.route('/add_msg', methods=['POST'])
@jwt_required
def add_msg():
    sender_email = request.form['sender']
    receiver_email = request.form['receiver']

    sender = User.query.filter_by(email=sender_email).first()
    receiver = User.query.filter_by(email=receiver_email).first()

    if not sender:
        return jsonify(f'Could not find user {sender_email}')
    if not receiver:
        return jsonify(f'Could not find user {receiver_email}')

    message_content = request.form['message']
    subject = request.form['subject']
    creation_date = request.form['creation_date']

    new_msg = Msg(msg_subject=subject,
                  msg_content=message_content,
                  msg_creation_date=creation_date)

    db.session.add(new_msg)
    db.session.flush()

    transaction = Transaction(msg_from=sender.id,
                              msg_to=receiver.id,
                              msg_index=new_msg.id,
                              msg_read=0)
    db.session.add(transaction)
    db.session.commit()

    return jsonify(message="You added a message"), 201

# Get all messages for a specific user
@app.route('/get_messages', methods=["GET"])
@jwt_required
def get_messages():
    if not session.get('user_id'):
        return jsonify(f'Please Login again')
    msg_list = Transaction.query.filter_by(msg_to=session.get('user_id')).all()
    if msg_list:
        messages_index = []

        for message in msg_list:
            message.msg_read = 1
            temp_msg = trans_schema.dump(message)
            messages_index.append(temp_msg.get('msg_index'))

        db.session.commit()
        messages_result = [Msg.query.filter_by(id=message_index).first() for message_index in messages_index]

        return jsonify(msgs_schema.dump(messages_result))
    else:
        return jsonify('No Messages for user: ' + session.get('email')), 404

# Get all unread messages for a specific user
@app.route('/get_new_messages', methods=["GET"])
@jwt_required
def get_new_messages():
    if not session.get('user_id'):
        return jsonify(f'Please Login again')
    msg_list = Transaction.query.filter_by(msg_to=session.get('user_id'), msg_read=0).all()
    if msg_list:
        messages_index = []

        for message in msg_list:
            message.msg_read = 1
            temp_msg = trans_schema.dump(message)
            messages_index.append(temp_msg.get('msg_index'))

        db.session.commit()
        messages_result = [Msg.query.filter_by(id=message_index).first() for message_index in messages_index]

        return jsonify(msgs_schema.dump(messages_result))
    else:
        return jsonify('No Messages for user: ' + session.get('email')), 404

# Read message (return one message)
@app.route('/get_message', methods=["GET"])
@jwt_required
def get_message():
    if not session.get('user_id'):
        return jsonify(f'Please Login again')
    msg = Transaction.query.filter_by(msg_to=session.get('user_id'), msg_read=0).first()
    if msg:
        msg.msg_read = 1
        db.session.commit()
        temp_msg = trans_schema.dump(msg)
        out_msg = Msg.query.filter_by(id=temp_msg.get('msg_index')).first()
        return jsonify(msg_schema.dump(out_msg))
    else:
        return jsonify('No Messages for user: ' + session.get('email')), 404

# Delete message (as owner or as receiver)
@app.route('/remove_message/<int:msg_id>', methods=['DELETE'])
@jwt_required
def remove_message(msg_id: int):
    msg = Msg.query.filter_by(id=msg_id).first()
    if msg:
        db.session.delete(msg)
        trans = Transaction.query.filter_by(msg_index=msg_id).first()
        db.session.delete(trans)
        db.session.commit()
        return jsonify(message="You deleted a message"), 202
    else:
        return jsonify(message="That message does not exist"), 404


if __name__ == '__main__':
    if not os.path.isfile(basedir + '/company_api.db'):
        db_create()
        db_seed()
    app.run()
