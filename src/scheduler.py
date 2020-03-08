import os
from sqlalchemy import create_engine, func, asc
from sqlalchemy.orm import sessionmaker
from models import Tournaments, Flights
from datetime import datetime, timedelta


engine = create_engine( os.environ.get('DATABASE_URL'))
Session = sessionmaker( bind=engine )
session = Session()


_17hrs_ago = datetime.utcnow() - timedelta(hours=17)
trmnts = session.query(Tournaments) \
            .filter( Tournaments.status == 'open') \
            .filter( Tournaments.flights.any(
                Flights.start_at < _17hrs_ago
            ))

if trmnts is not None:
    for trmnt in trmnts:
        latest_flight = trmnt.flights.pop()
        if latest_flight.start_at < _17hrs_ago:
            trmnt.status = 'waiting_results'


session.commit()


