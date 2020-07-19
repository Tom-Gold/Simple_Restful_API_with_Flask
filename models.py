from app import db, ma
from sqlalchemy import Column, Integer, String
# from flask import Blueprint

# models_bp = Blueprint('models_bp', ' __name__')


# database models
class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)


class Msg(db.Model):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    msg_subject = Column(String)
    msg_content = Column(String)
    msg_creation_date = Column(String)


class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    msg_from = Column(Integer)
    msg_to = Column(Integer)
    msg_index = Column(Integer)
    msg_read = Column(Integer)


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email', 'password')


class MsgSchema(ma.Schema):
    class Meta:
        fields = ('msg_id', 'msg_subject', 'msg_content', 'msg_creation_date')


class TransactionSchema(ma.Schema):
    class Meta:
        fields = ('trans_id', 'msg_from', 'msg_to', 'msg_index', 'msg_read')


user_schema = UserSchema()
users_schema = UserSchema(many=True)

msg_schema = MsgSchema()
msgs_schema = MsgSchema(many=True)

trans_schema = TransactionSchema()
transactions_schema = TransactionSchema(many=True)


# Creates the database
# @app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database created!')


# Clears the database
# @app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database dropped!')


# Seeding the database
# @app.cli.command('db_seed')
def db_seed():
    test_msg_1 = Msg(msg_subject='test_msg_1 subject',
                     msg_content='test_msg_1 content',
                     msg_creation_date='1/1/20')

    test_msg_2 = Msg(msg_subject='test_msg_2 subject',
                     msg_content='test_msg_2 content',
                     msg_creation_date='1/1/20')

    test_msg_3 = Msg(msg_subject='test_msg_3 subject',
                     msg_content='test_msg_3 content',
                     msg_creation_date='1/1/20')

    db.session.add(test_msg_1)
    db.session.add(test_msg_2)
    db.session.add(test_msg_3)

    test_user_sender = User(first_name='William',
                            last_name='sender',
                            email='test@test.com',
                            password='P@ssw0rd')

    test_user_receiver = User(first_name='William',
                              last_name='receiver',
                              email='test_rec@test.com',
                              password='P@ssw0rd')
    db.session.add(test_user_sender)
    db.session.add(test_user_receiver)

    db.session.flush()

    test_transaction = Transaction(msg_from=test_user_sender.id,
                                   msg_to=test_user_receiver.id,
                                   msg_index=test_msg_1.id,
                                   msg_read=0)

    db.session.add(test_transaction)
    db.session.commit()
    print('Database seeded!')