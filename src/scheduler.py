import os
from sqlalchemy import create_engine, func
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

# for trmnt in trmnts:
#     change_status = True
#     for flight in trmnt.flights:
#         if flight.start_at > _17hrs_ago:
#             change_status = False
#     if change_status:
#         trmnt.status = 'waiting_results'

# session.commit()


