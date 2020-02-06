import os
import models as m
from models import db, Users
from datetime import datetime, timedelta
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# an Engine, which the Session will use for connection
# resources
engine = create_engine('postgres://Francine@localhost/swapprofit')

# create a configured "Session" class
Session = sessionmaker(bind=engine)

# create a Session
session = Session()

session = Session.object_session(Users)
# users = Session.query(Users).get(1)



# metadata = MetaData()
# connection = engine.connect()

# users = Table('users', metadata, autoload=True, autoload_with=engine)
# print( repr(users) )





