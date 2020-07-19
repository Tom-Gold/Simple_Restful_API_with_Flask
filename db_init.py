# # from app import db
# from models import Msg, Transaction, User
#
#
# # Creates the database
# # @app.cli.command('db_create')
# def db_create(db):
#     db.create_all()
#     print('Database created!')
#
#
# # Clears the database
# # @app.cli.command('db_drop')
# def db_drop(db):
#     db.drop_all()
#     print('Database dropped!')
#
#
# # Seeding the database
# # @app.cli.command('db_seed')
# def db_seed(db):
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