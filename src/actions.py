import os
import json
import utils
import requests
from sqlalchemy import or_
from utils import isfloat
from datetime import datetime
from models import db, Profiles, Buy_ins, Swaps, Tournaments, Flights


def swap_tracker_json(trmnt, user_id):
    
    my_buyin = Buy_ins.get_latest( user_id=user_id, tournament_id=trmnt.id )
    final_profit = 0

    swaps = Swaps.query.filter_by(
        sender_id = user_id,
        tournament_id = trmnt.id
    )

    # separate swaps by recipient id
    swaps_by_recipient = {}
    for swap in swaps:
        rec_id = str(swap.recipient_id)
        data = swaps_by_recipient.get( rec_id, [] )
        swaps_by_recipient[ rec_id ] = [ *data, swap ]
    
    # Loop through swaps to create swap tracker json and append to 'swaps_buyins'
    swaps_buyins = []
    for rec_id, swaps in swaps_by_recipient.items():
        recipient_buyin = Buy_ins.get_latest(
                user_id = rec_id,
                tournament_id = trmnt.id
            )

        # Catch ERRORS
        if recipient_buyin is None or my_buyin is None:
            swap_data_for_error_message = [{
                'recipient_name': f'{x.recipient_user.first_name} {x.recipient_user.last_name}',
                'sender_name': f'{x.sender_user.first_name} {x.sender_user.last_name}',
                'tournament_name': x.tournament.name 
            } for x in swaps]
            if recipient_buyin is None:
                return { 
                    'ERROR':'Recipient has swaps with user in this tournament but no buy-in',
                    'recipient buyin': None,
                    'swaps with user': swap_data_for_error_message }
            if my_buyin is None:
                return { 
                    'ERROR':'User has swaps in this tournament but no buy-in',
                    'buyin': None,
                    'user swaps': swap_data_for_error_message }

        # Structure and fill most properties for swap tracker json
        recipient_user = Profiles.query.get( rec_id )
        data = {
            'recipient_user': recipient_user.serialize(),
            'recipient_buyin': recipient_buyin.serialize(),
            'their_place': recipient_buyin.place,
            'you_won': my_buyin.winnings if my_buyin.winnings else 0,
            'they_won': recipient_buyin.winnings if recipient_buyin.winnings else 0,
            'available_percentage': recipient_user.available_percentage(trmnt.id),
            'agreed_swaps': [],
            'other_swaps': []
        }

        # Fill in properties: 'agreed_swaps' and 'other_swaps' lists
        you_owe_total = 0
        they_owe_total = 0
        for swap in swaps:
            single_swap_data = { **swap.serialize(),
                'counter_percentage': swap.counter_swap.percentage }
            
            if swap.status._value_ == 'agreed':
                you_owe = ( float(my_buyin.winnings) * swap.percentage / 100 ) \
                    if isfloat(my_buyin.winnings) else 0
                they_owe = ( float(recipient_buyin.winnings) 
                    * swap.counter_swap.percentage / 100 ) \
                    if isfloat(recipient_buyin.winnings) else 0
                you_owe_total += you_owe
                they_owe_total += they_owe
                data['agreed_swaps'].append({
                    **single_swap_data,
                    'you_owe': you_owe,
                    'they_owe': they_owe
                })
            else:
                data['other_swaps'].append(single_swap_data)

        # Fill in final properties
        data['you_owe_total'] = you_owe_total
        data['they_owe_total'] = they_owe_total
        final_profit -= you_owe_total
        final_profit += they_owe_total

        # Append json
        swaps_buyins.append(data)


    return {
        'tournament': trmnt.serialize(),
        'my_buyin': my_buyin and my_buyin.serialize(),
        'buyins': swaps_buyins,
        'final_profit': final_profit
    }





def load_tournament_file():


    path = os.environ['APP_PATH']
    with open( path + '/src/files/tournaments.json' ) as f:
        data = json.load( f )


    # casino cache so not to request for same casinos
    path_cache = os.environ['APP_PATH'] + '/src/files/casinos.json'
    if os.path.exists( path_cache ):
        with open( path_cache ) as f:
            cache = json.load(f)
    else: cache = {}

    casino_ref = ['address','city','state','zip_code','longitude',
        'latitude','time_zone']


    for r in data:
        
        # Do not add these to Swap Profit
        if r['Tournament'].strip() == '' or \
        'satelite' in r['Tournament'].lower() or \
        r['Results Link'] == False:
            continue

        trmnt = Tournaments.query.get( r['Tournament ID'] )
        trmnt_name, flight_day = utils.resolve_name_day( r['Tournament'] )
        start_at = datetime.strptime(
            r['Date'][:10] + r['Time'], 
            '%Y-%m-%d%H:%M:%S' )

        ref = {
            'name': trmnt_name, 
            'start_at': start_at,
            'results_link': r['Results Link'] 
        }
        flight_ref = { 
            'start_at': start_at, 
            'day': flight_day }


        if trmnt is None:

            casino = cache.get( r['Casino ID'] )
            
            # Create tournament
            trmnt = Tournaments(
                id = r['Tournament ID'],
                **{ db_col: val for db_col, val in ref.items() },
                **{ db_col: casino[db_col] for db_col in casino_ref }
            )
            db.session.add( trmnt )
            db.session.commit()
            
            # Create flight
            db.session.add( Flights( **flight_ref, tournament_id=trmnt.id ))

            db.session.commit()

        else:
            for db_col, val in ref.items():
                if getattr(trmnt, db_col) != val:
                    setattr(trmnt, db_col, val)

            flight = Flights.query.filter_by( tournament_id=trmnt.id ) \
                .filter( or_( Flights.day == flight_day, Flights.start_at == start_at )) \
                .first()

            # Create flight
            if flight is None:
                db.session.add( Flights( **flight_ref, tournament_id=trmnt.id ))
            
            # Update flight
            else:
                for db_col, val in flight_ref.items():
                    if getattr(flight, db_col) != val:
                        setattr(flight, db_col, val)

            db.session.commit()

    return True