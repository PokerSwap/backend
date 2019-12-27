from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc, desc
from datetime import datetime
import enum

db = SQLAlchemy()



class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    valid = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    profile = db.relationship('Profiles', back_populates='user', uselist=False)

    def __repr__(self):
        return f'<Users {self.email}>'

    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'valid': self.valid,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }



class Profiles(db.Model):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    nickname = db.Column(db.String(100))
    hendon_url = db.Column(db.String(200))
    profile_pic_url = db.Column(db.String(250), default=None)
    roi = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('Users', back_populates='profile', uselist=False)
    buy_ins = db.relationship('Buy_ins', back_populates='user')
    transactions = db.relationship('Transactions', back_populates='user')
    devices = db.relationship('Devices', back_populates='user')
    # sending_swaps
    # receiving_swaps

    def __repr__(self):
        return f'<Profiles {self.first_name} {self.last_name}>'

    def get_coins(self):
        total = 0
        for transaction in self.transactions:
            total += transaction.coins
        return total

    def available_percentage(self, tournament_id):
        status_to_consider = ['pending','agreed']
        total = 0
        for swap in self.sending_swaps:
            if swap.tournament_id == tournament_id:
                if swap.status._value_ in status_to_consider:
                    total += swap.percentage
        return 50 - total

    def get_swaps_actions(self, tournament_id):
        status_to_consider = ['pending','agreed']
        actions = 0
        swaps = 0
        for swap in self.sending_swaps:
            if swap.tournament_id == tournament_id:
                if swap.status._value_ in status_to_consider:
                    actions += swap.percentage
                    swaps += 1
        return {
            'actions': actions,
            'swaps': swaps
        }

    def serialize(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'nickname': self.nickname,
            'email': self.user.email,
            'profile_pic_url': self.profile_pic_url,
            'hendon_url': self.hendon_url,
            'roi': self.roi,
            'coins': self.get_coins(),
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'transactions': [x.serialize() for x in self.transactions],
            'devices': [x.serialize() for x in self.devices]
        }



class SwapStatus(enum.Enum):
    pending = 'pending'
    incoming = 'incoming'
    agreed = 'agreed'
    rejected = 'rejected'
    canceled = 'canceled'

class Swaps(db.Model):
    __tablename__ = 'swaps'
    id = db.Column(db.Integer, primary_key=True)
    counter_swap_id = db.Column(db.Integer, db.ForeignKey('swaps.id'))
    sender_id = db.Column(db.Integer, db.ForeignKey('profiles.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('profiles.id'))
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournaments.id'))
    percentage = db.Column(db.Integer, nullable=False)
    due_at = db.Column(db.DateTime, default=None)
    paid = db.Column(db.Boolean, default=False)
    cost = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = db.Column(db.Enum(SwapStatus), default=SwapStatus.pending)
    
    tournament = db.relationship('Tournaments', back_populates='swaps')
    sender_user = db.relationship('Profiles', foreign_keys=[sender_id], backref='sending_swaps')
    recipient_user = db.relationship('Profiles', foreign_keys=[recipient_id], backref='receiving_swaps')
    counter_swap = db.relationship('Swaps', remote_side=[id], post_update=True, uselist=False,
                                            backref='counter_swap2')

    def __repr__(self):
        return (f'<Swaps sender_email:{self.sender_user.user.email} ' 
            + f'recipient_email:{self.recipient_user.user.email} '
            + f'tournament:{self.tournament.name}>')

    @staticmethod
    def counter_status(status):
        if status == 'pending':
            return 'incoming'
        if status == 'incoming':
            return 'pending'
        return status

    def serialize(self):
        return {
            'id': self.id,
            'tournament_id': self.tournament_id,
            'percentage': self.percentage,
            'due_at': self.due_at,
            'status': self.status._value_,
            'sender_user': self.sender_user.serialize(),
            'recipient_user': self.recipient_user.serialize(),
            'paid': self.paid,
            'cost': self.cost,
            'counter_swap_id': self.counter_swap_id,
            'counter_percentage': self.counter_swap.percentage,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }



class Tournaments(db.Model):
    __tablename__ = 'tournaments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    address = db.Column(db.String(200))
    city = db.Column(db.String(50))
    state = db.Column(db.String(20))
    zip_code = db.Column(db.String(14))
    start_at = db.Column(db.DateTime)
    end_at = db.Column(db.DateTime)
    results_link = db.Column(db.String(256))
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    flights = db.relationship('Flights', back_populates='tournament')
    swaps = db.relationship('Swaps', back_populates='tournament')

    def __repr__(self):
        return f'<Tournament {self.name}>'

    @staticmethod
    def get_user_live_upcoming(user_id):
        now = datetime.utcnow()
        trmnts = (Tournaments.query
                    .filter( Tournaments.end_at > now )
                    .filter( Tournaments.flights.any( 
                        Flights.buy_ins.any( user_id = user_id )))
                    .order_by( Tournaments.start_at.asc() ))
        return trmnts if trmnts.count() > 0 else None

    @staticmethod
    def get_user_history(user_id):
        now = datetime.utcnow()
        trmnts = (Tournaments.query
                    .filter( Tournaments.flights.any( 
                        Flights.buy_ins.any( user_id = user_id )))
                    .filter( Tournaments.end_at < now )
                    .order_by( Tournaments.start_at.desc() ))
        return trmnts if trmnts.count() > 0 else None

    def get_all_users_latest_buyins(self):
        all_buyins = Buy_ins.query.filter( 
                        Buy_ins.flight.has( 
                            Flights.tournament_id == self.id ))
        user_ids = []
        buyins = []
        for buyin in all_buyins:
            user_id = buyin.user_id
            # Users may have multiple buy_ins in one tournament
            if user_id not in user_ids:
                user_ids.append( user_id )
                buyins.append( Buy_ins.get_latest(user_id, self.id).serialize() )
        return buyins

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'start_at': self.start_at,
            'end_at': self.end_at,
            'longitude': self.longitude,
            'latitude': self.latitude,
            'results_link': self.results_link,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'flights': [x.serialize() for x in self.flights],
            'swaps': [x.serialize() for x in self.swaps],
            'buy_ins': self.get_all_users_latest_buyins()
        }



class Flights(db.Model):
    __tablename__ = 'flights'
    id = db.Column(db.Integer, primary_key=True)
    start_at = db.Column(db.DateTime)
    end_at = db.Column(db.DateTime)
    day = db.Column(db.Integer)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournaments.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    tournament = db.relationship('Tournaments', back_populates='flights')
    buy_ins = db.relationship('Buy_ins', back_populates='flight')

    def __repr__(self):
        return f'<Flights tournament:{self.tournament.name} {self.start_at} - {self.end_at}>'

    def serialize(self):
        return {
            'id': self.id,
            'tournament_id': self.tournament_id,
            'tournament': self.tournament.name,
            'start_at': self.start_at,
            'end_at': self.end_at,
            'day': self.day,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }



class Buy_ins(db.Model):
    __tablename__ = 'buy_ins'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('profiles.id'))
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.id'))
    receipt_img_url = db.Column(db.String(250))
    chips = db.Column(db.Integer)
    table = db.Column(db.Integer)
    seat = db.Column(db.Integer)
    place = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('Profiles', back_populates='buy_ins')
    flight = db.relationship('Flights', back_populates='buy_ins')

    def __repr__(self):
        return f'<Buy_ins id:{self.id} user:{self.user_id} flight:{self.flight_id}>'

    @staticmethod
    def get_latest(user_id, tournament_id):
        return (Buy_ins.query
            .filter( Buy_ins.flight.has( tournament_id=tournament_id ))
            .filter_by( user_id=user_id )
            .order_by( Buy_ins.id.desc() ).first())

    def serialize(self):
        u = self.user
        return {
            'id': self.id,
            'user_id': self.user_id,
            'flight_id': self.flight_id,
            'tournament_id': self.flight.tournament_id,
            'place': self.place,
            'chips': self.chips,
            'table': self.table,
            'seat': self.seat,
            'receipt_img_url': self.receipt_img_url,
            'user_name': u.nickname if u.nickname else f'{u.first_name} {u.last_name}',
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }



class Transactions(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('profiles.id'))
    coins = db.Column(db.Integer, nullable=False)
    dollars = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('Profiles', back_populates='transactions')

    def __repr__(self):
        return f'<Transactions user:{self.user.email} coins:{self.coins} dollars:{self.dollars}>'

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'coins': self.coins,
            'dollars': self.dollars,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }



class Devices(db.Model):
    __tablename__ = 'devices'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('profiles.id'))
    token = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('Profiles', back_populates='devices')

    def __repr__(self):
        return f'<Devices id:{self.id} user_email:{self.user.email}>'

    def serialize(self):
        return {
            'id': self.id,
            'token': self.token,
            'user_id': self.user_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
