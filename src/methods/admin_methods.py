import os
import json
import seeds
import utils
import requests
from flask import request, jsonify
from flask_jwt_simple import JWTManager, create_jwt, get_jwt, jwt_required
from sqlalchemy import desc, or_
from utils import APIException, role_jwt_required
from models import db, Profiles, Tournaments, Swaps, Flights, Buy_ins, Devices
from datetime import datetime

def attach(app):



    @app.route('/reset_database')
    @jwt_required
    def run_seeds():

        if get_jwt()['role'] != 'admin':
            raise APIException('Access denied', 403)

        seeds.run()

        lou = Profiles.query.filter_by(nickname='Lou').first()

        return jsonify({
            "1 Lou's id": lou.id,
            "2 token_data": {
                "id": lou.id,
                "role": "admin",
                "exp": 600000
            },
            "3 token": create_jwt({
                    'id': lou.id,
                    'role': 'admin',
                    'exp': 600000
                })
        })




    @app.route('/tournaments', methods=['POST'])
    # @role_jwt_required(['admin'])
    def add_tournaments():


        # casino cache so not to request for same casinos
        path_cache = os.environ['APP_PATH'] + '/src/jsons/tournaments.json'
        if os.path.exists( path_cache ):
            with open( path_cache ) as f:
                cache = json.load( f )
        else: cache = {}


        # data comes in as a string
        data = json.loads( request.get_json() )

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


            trmntjson = { 
                'id': r['Tournament ID'],
                'name': trmnt_name, 
                'start_at': start_at,
                'results_link': str( r['Results Link'] ).strip()
            }
            flightjson = {
                'start_at':start_at,
                'day': flight_day
            }


            if trmnt is None:

                casino = cache.get( r['Casino ID'] )
                
                if casino is None:
                    rsp = requests.get( 
                        f"{os.environ['POKERSOCIETY_HOST']}/casinos/{r['Casino ID']}" )
                    if not rsp.ok:
                        raise APIException(f'Casino with id "{r["Casino ID"]}" not found', 404)               
                    
                    casino = rsp.json()
                    cache[ r['Casino ID'] ] = casino


                trmntjson = {
                    **trmntjson,
                    'address': casino['address'].strip,
                    'city': casino['city'].strip,
                    'state': casino['state'].strip,
                    'zip_code': str( casino['zip_code'] ).strip,
                    'longitude': float( casino['longitude'] ),
                    'latitude': float( casino['latitude'] )
                }


                # Create tournament
                trmnt = Tournaments( **trmntjson )
                db.session.add( trmnt )
                db.session.flush()
                
                # Create flight
                db.session.add( Flights(
                    tournament_id=trmnt.id, 
                    **flightjson
                ))

            else:
                # Update tournament
                for db_col, val in trmntjson.items():
                    if db_col != 'start_at':
                        if getattr(trmnt, db_col) != val:
                            setattr(trmnt, db_col, val)

                flight = Flights.query.filter_by( tournament_id=trmnt.id ) \
                    .filter( or_( Flights.day == flight_day, Flights.start_at == start_at )) \
                    .first()

                # Create flight
                if flight is None:
                    db.session.add( Flights( 
                        tournament_id=trmnt.id,
                        **flightjson
                    ))
                
                # Update flight
                else:
                    for db_col, val in flightjson.items():
                        if getattr(flight, db_col) != val:
                            setattr(flight, db_col, val)

        db.session.commit()

        # Save cache
        if cache != {}:
            with open( path_cache, 'w' ) as f:
                json.dump( cache, f, indent=2 )

        return jsonify({'message':'Tournaments have been updated'}), 200




    @app.route('/results', methods=['POST'])
    def get_results():
        
        '''
        results = {
            "tournament_id": 45,
            "tournament_buy_in": 150,
            "tournament_date": "23 Aug, 2020",
            "tournament_name": "Las Vegas Live Night Hotel",
            "results_link": "https://poker-society.herokuapp.com/results_link/234"
            "users": {
                "sdfoij@yahoo.com": {
                    "position": 11,
                    "winnings": 200,
                    "total_winning_swaps": 34
                }
            }
        }
        '''

        results  = request.get_json()

        trmnt = Tournaments.query.get( 45 )
        trmnt.results_link = results['results_link']
        trmnt.status = 'closed'
        db.session.commit()

        for email, user_result in results['users'].items():
            
            user = Profiles.query.filter( 
                        Profiles.user.email == email ).first()

            # Consolidate swaps if multiple with same user
            all_agreed_swaps = user.get_agreed_swaps( results['tournament_id'] )
            swaps = {}
        
            for swap in all_agreed_swaps:
                id = str( swap.recipient_id )
                if id not in swaps:
                    swaps[id] = {
                        'count': 1,
                        'percentage': swap.percentage,
                        'counter_percentage': swap.counter_swap.percentage
                    }
                else:
                    x = swaps[id]
                    swaps[id] = {
                        'count': x['count'] + 1,
                        'percentage': x['percentage'] + swap.percentage,
                        'counter_percentage': x['counter_percentage'] + \
                                                swap.counter_swap.percentage
                    }

            # Create the swap templates
            msg = lambda x: \
                f'You have {x} swaps with this person for the following total amounts:'
            
            total_swap_earnings = 0
            render_swaps = ''
            swap_number = 1

            for swap in swaps:
                recipient_email = swap.recipient_user.user.email
                recipient = Profiles.query.filter( Profiles.user.email == recipient_email )

                entry_fee = results['tournament_buy_in']
                profit_sender = user_result['winnings'] - entry_fee
                amount_owed_sender = profit_sender * swap['percentage'] / 100
                earning_recipient = results[ recipient_email ]['winnings']
                profit_recipient = earning_recipient - entry_fee
                amount_owed_recipient = profit_recipient * swap['counter_percentage'] / 100

                swap_data = {
                    'swap_number': swap_number,
                    'amount_of_swaps': msg(swap['count']) if swap['count'] > 1 else '',
                    'entry_fee': entry_fee,
                    
                    'total_earnings_sender': user_result['winnings'],
                    'swap_percentage_sender': swap['percentage'],
                    'swap_profit_sender': profit_sender,
                    'amount_owed_sender': amount_owed_sender,

                    'recipient_name': f'{recipient.firt_name} {recipient.last_name}',
                    'recipient_profile_pic_url': recipient.profile_pic_url,
                    'total_earnings_recipient': earning_recipient,
                    'swap_percentage_recipient': swap['counter_percentage'],
                    'swap_profit_recipient': profit_recipient,
                    'amount_owed_recipient': amount_owed_recipient
                }
                
                total_swap_earnings -= amount_owed_sender
                total_swap_earnings += amount_owed_recipient
                render_swaps += render_template('swap.html', **swap_data)
                swap_number += 1

            # Update user and buy ins
            user.calculate_total_swaps_save()
            user.roi_rating = user_result['total_winning_swaps'] / user.total_swaps * 100

            buyin = Buy_ins.get_latest( user.id, trmnt.id )
            buyin.place = user_result['position']

            db.session.commit()


            sign = '-' if total_swap_earnings < 0 else '+'
            send_email('swap_results','hernanjkd@gmail.com',
                data={
                    'tournament_date': results['tournament_date'],
                    'tournament_name': results['tournament_name'],
                    'results_link': results['results_link'],
                    'total_swaps': swap_number,
                    'total_swap_earnings': f'{sign}${str(abs(total_swap_earnings))}',
                    'render_swaps': render_swaps,
                    'roi_rating': user.roi_rating,
                    'swap_rating': user.swap_rating
                })




    @app.route('/create/token', methods=['POST'])
    def create_token():
        return jsonify( create_jwt(request.get_json()) ), 200




    @app.route('/tournaments', methods=['POST'])
    def add_tournament():
        req = request.get_json()
        db.session.add(Tournaments(
            name = req['name'],
            address = req['address'],
            start_at = datetime( *req['start_at'] ),
            end_at = datetime( *req['end_at'] ),
            longitude = None,
            latitude = None
        ))
        db.session.commit()
        search = {
            'name': req['name'],
            'start_at': datetime( *req['start_at'] )
        }
        return jsonify(Tournaments.query.filter_by(**search).first().serialize()), 200




    @app.route('/flights/<int:id>')
    def get_flights(id):
        if id == 'all':
            return jsonify([x.serialize() for x in Flights.query.all()])

        if id.isnumeric():
            flight = Flights.query.get(int(id))
            if flight is None:
                raise APIException('Flight not found', 404)
            return jsonify(flight.serialize())
        
        return jsonify({'message':'Invalid id'})




    @app.route('/flights', methods=['POST'])
    def create_flight():
        req = request.get_json()
        db.session.add(Flights(
            tournament_id = req['tournament_id'],
            start_at = datetime( *req['start_at'] ),
            end_at = datetime( *req['end_at'] ),
            day = req['day']
        ))
        db.session.commit()
        search = {
            'tournament_id': req['tournament_id'],
            'start_at': datetime(*req['start_at']),
            'end_at': datetime(*req['end_at']),
            'day': req['day']
        }
        return jsonify(Flights.query.filter_by(**search).first().serialize()), 200



    @app.route('/swaps/<int:id>')
    def get_swaps_tool(id):
        swap = Swaps.query.get( id )
        if swap is None:
            raise APIException('Swap not found', 404)
        return jsonify(swap.serialize())




    @app.route('/users/me/devices', methods=['DELETE'])
    @role_jwt_required(['user'])
    def delete_device(user_id):
        
        req = request.get_json()
        utils.check_params(req, 'device_token')
        
        devices = Devices.query.filter_by( token=req['device_token'] )
        for device in devices:
            db.session.delete( device )
            db.session.commit()
        
        return jsonify({'message':'Device deleted successfully'})




    @app.route('/buy_ins/<id>')
    def get_buyins(id):
        if id == 'all':
            return jsonify([x.serialize() for x in Buy_ins.query.all()])
        return jsonify(Buy_ins.query.get(int(id)).serialize())




    @app.route('/buy_ins/<int:id>', methods=['PUT'])
    def update_buyins_tool(id):
        buyin = Buy_ins.query.get(id)
        r = request.get_json()
        buyin.place = r.get('place')
        buyin.winnings = r.get('winnings')
        db.session.commit()
        return jsonify({**buyin.serialize(),'winnings':buyin.winnings})




    @app.route('/flights/<int:id>', methods=['DELETE'])
    @role_jwt_required(['admin'])
    def delete_flight(id, **kwargs):
        db.session.delete( Flights.query.get(id) )
        db.session.commit()
        return jsonify({'message':'Flight deleted'}), 200




    @app.route('/tournaments/<int:id>', methods=['DELETE'])
    @role_jwt_required(['admin'])
    def delete_tournament(id, **kwargs):
        db.session.delete( Tournaments.query.get(id) )
        db.session.commit()
        return jsonify({'message':'Tournament deleted'}), 200




    @app.route('/buy_ins/<int:id>', methods=['DELETE'])
    @role_jwt_required(['admin'])
    def delete_buy_in(id, **kwargs):
        db.session.delete( Buy_ins.query.get(id) )
        db.session.commit()
        return jsonify({'message':'Buy in deleted'}), 200




    @app.route('/swaps', methods=['DELETE'])
    @role_jwt_required(['admin'])
    def delete_swap(**kwargs):
        req = request.get_json()
        db.session.delete( Swaps.query.get(req['sender_id'], req['recipient_id'], req['tournament_id']) )
        db.session.commit()
        return jsonify({'message':'Swap deleted'}), 200




    @app.route('/users/me/devices', methods=['POST'])
    @role_jwt_required(['user'])
    def add_device(user_id):
        req = request.get_json()
        utils.check_params(req, 'device_token')
        db.session.add(Devices(
            user_id = user_id,
            token = req['device_token'] ))
        db.session.commit()
        return jsonify({'message':'Device added successfully'})




    @app.route('/swaps/all', methods=['GET'])
    @role_jwt_required(['admin'])
    def get_swaps(**kwargs):
        
        return jsonify([x.serialize() for x in Swaps.query.all()])





    return app