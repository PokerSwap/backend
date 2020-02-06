import os
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from models import Tournaments, Flights
from datetime import datetime, timedelta


engine = create_engine('postgres://Francine@localhost/swapprofit')
Session = sessionmaker(bind=engine)
session = Session()

country = Tournaments(
    name='Coconut Creek - NLH Survivor $2,000 Guaranteed',
    address='287 Carrizo Canyon Rd',
    city='Mescalero',
    state='NM',
    zip_code='12084',
    latitude=33.2956,
    longitude=-105.6901,
    start_at=datetime(2018,12,29,10)
)
flight1_country = Flights(
    start_at=datetime(2018,12,29,10),
    tournament= country
)
flight2_country = Flights(
    start_at=datetime(2020,12,29,10),
    tournament= country
)
# db.session.add_all([country, flight1_country])

_17hrs_ago = datetime.utcnow() - timedelta(hours=17)
trmnts = session.query(Tournaments) \
            .filter( Tournaments.status == 'waiting_results')
            # .filter( Tournaments.flights.any( 
            #     func.max(Flights.start_at) < _17hrs_ago ))
            # .filter( Tournaments.flights)

for t in [x for x in trmnts]:
    print(t.status._value_)



# session = Session.object_session(Users)
# users = Session.query(Users).get(1)



# metadata = MetaData()
# connection = engine.connect()

# users = Table('users', metadata, autoload=True, autoload_with=engine)
# print( repr(users) )





