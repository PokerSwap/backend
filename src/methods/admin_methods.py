import utils
from flask import request, jsonify
from flask_jwt_simple import JWTManager, create_jwt, get_jwt, jwt_required
from sqlalchemy import desc
from utils import APIException, role_jwt_required
from models import db, Profiles, Tournaments, Swaps, Flights, Buy_ins
from datetime import datetime
from reset_database import run_seeds

def attach(app):


    @app.route('/tournaments', methods=['POST'])
    @role_jwt_required(['admin'])
    def add_tournaments(user_id):
        
        trmnt_list = request.get_json()
        
        for coming_trmnt in trmnt_list:
            
            trmnt = Tournaments.query.get( coming_trmnt['id'] )

            if trmnt is None:
                db.session.add( Tournaments(
                    id = coming_trmnt['id'],
                    name = coming_trmnt['tournament'],
                    address = coming_trmnt['address'],
                    city = coming_trmnt['city'],
                    state = coming_trmnt['state'],
                    zip_code = coming_trmnt['zip_code'],
                    start_at = coming_trmnt['start_at'],
                    results_link = coming_trmnt['results link'],
                    longitude = coming_trmnt['longitude'],
                    latitude = coming_trmnt['latitude']
                ))

            else:
                db_fields = {'name':'tournament','address':'address',
                    'city':'city','state':'state','zip_code':'zip_code',
                    'start_at':'start_at','results_link':'results link',
                    'longitude':'longitude','latitude':'latitude'}
                for db_name, entry_name in db_fields.items():
                    if getattr(trmnt, db_name) != coming_trmnt[entry_name]:
                        setattr(trmnt, db_name, coming_trmnt[entry_name])
            
            db.session.commit()

        return jsonify({'message':'Tournament csv has been proccessed successfully'}), 200



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



    @app.route('/reset_database')
    @jwt_required
    def populate():

        if get_jwt()['role'] != 'admin':
            raise APIException('Access denied', 403)

        run_seeds()

        lou = Profiles.query.filter_by(nickname='Lou').first()

        return jsonify([
            {"Lou's id": lou.id},
            {"token_data": {
                "id": lou.id,
                "role": "admin",
                "exp": 600000
            }},
            {"token": create_jwt({
                        'id': lou.id,
                        'role': 'admin',
                        'exp': 600000
                    })}
        ])




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




    @app.route('/users/me/devices', methods=['DELETE'])
    @role_jwt_required(['user'])
    def delete_device(user_id):
        
        req = request.get_json()
        utils.check_params(req, 'device_token')
        
        devices = Buy_ins.query.filter_by( token=req['device_token'] )
        for device in devices:
            db.session.delete( device )
            db.session.commit()
        
        return jsonify({'message':'Device deleted successfully'})




    @app.route('/buy_ins/<id>')
    def get_buyins(id):
        if id == 'all':
            return jsonify([x.serialize() for x in Buy_ins.query.all()])
        return jsonify(Buy_ins.query.get(int(id)).serialize())




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
