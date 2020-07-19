from app import db, ma
from sqlalchemy import Column, Integer, String


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