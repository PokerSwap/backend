import os
import json
import regex
import utils
import actions
import cloudinary
import cloudinary.uploader
from google.cloud import vision
from datetime import datetime, timedelta
from flask import request, jsonify, render_template
from flask_jwt_simple import create_jwt, decode_jwt, get_jwt
from sqlalchemy import desc, asc
from utils import APIException, role_jwt_required, isfloat
from models import (db, Users, Profiles, Tournaments, Swaps, Flights, 
    Buy_ins, Transactions, Devices)
from notifications import send_email, send_fcm


def attach(app):
    
    
    @app.route('/users/me/email', methods=['PUT'])
    @role_jwt_required(['user'])
    def update_email(user_id):
        
        req = request.get_json()
        utils.check_params(req, 'email', 'password', 'new_email')

        if req['email'] == req['new_email']:
            return jsonify({'message':'Your email is already '+req['new_email']})

        user = Users.query.filter_by( 
            id = user_id, 
            email = req['email'], 
            password = utils.sha256(req['password']) 
        ).first()
        
        if user is None:
            raise APIException('User not found', 404)

        user.status = 'invalid'
        user.email = req['new_email']

        db.session.commit()

        send_email( template='email_validation', emails=user.email, 
            data={'validation_link': utils.jwt_link(user.id, role='email_change')} )

        return jsonify({'message': 'Please verify your new email'}), 200




    @app.route('/users/reset_password/<token>', methods=['GET','PUT'])
    def html_reset_password(token):

        jwt_data = decode_jwt(token)
        
        if request.method == 'GET':
            user = Users.query.filter_by(
                id = jwt_data['sub'], 
                email = jwt_data['role']).first()
            if user is None:
                raise APIException('User not found', 404)

            return render_template('reset_password.html',
                host = os.environ.get('API_HOST'),
                token = token,
                email = jwt_data['role']
            )
        
        # request.method == 'PUT'
        req = request.get_json()
        utils.check_params(req, 'email', 'password')

        if len( req['password'] ) < 6:
            raise APIException('Password must be at least 6 characters long')

        user = Users.query.filter_by(
            id = jwt_data['sub'],
            email = req['email']
        )
        if user is None:
            raise APIException('User not found', 404)

        user.password = utils.sha256(req['password'])

        db.session.commit()

        return jsonify({'message': 'Your password has been updated'}), 200




    @app.route('/users/me/password', methods=['PUT'])
    def reset_password():

        req = request.get_json()
        utils.check_params(req, 'email')

        # User forgot their password
        if request.args.get('forgot') == 'true':
            user = Users.query.filter_by( email=req['email'] ).first()
            if user is None:
                raise APIException('This email is not registered', 400)

            send_email('reset_password_link', emails=req['email'], 
                data={'link':utils.jwt_link(user.id, 'users/reset_password/', req['email'])})
            return jsonify({
                'message': 'A link has been sent to your email to reset the password'
            }), 200

        # User knows their password
        utils.check_params(req, 'password', 'new_password')

        if req['password'] == req['new_password']:
            raise APIException('Your new password is the same as the old password')
        if len( req['new_password'] ) < 6:
            raise APIException('Your new password must be at least 6 characters long')

        user = Users.query.filter_by(
            email=req['email'],
            password=utils.sha256(req['password'])
        ).first()
        if user is None:
            raise APIException('User not found', 404)

        user.password = utils.sha256(req['new_password'])

        db.session.commit()

        return jsonify({'message': 'Your password has been changed'}), 200




    @app.route('/users/invite', methods=['POST'])
    @role_jwt_required(['user'])
    def invite_users(user_id):

        req = request.get_json()
        utils.check_params(req, 'email')

        user = Users.query.get( user_id )

        send_email('invitation_email', emails=req['email'], data={
            'user_name': f'{user.first_name} {user.last_name}'
        })

        return jsonify({'message':'Invitation sent successfully'})




    # id can be the user id, 'me' or 'all'
    @app.route('/profiles/<id>', methods=['GET'])
    @role_jwt_required(['user'])
    def get_profiles(user_id, id):
        
        jwt_data = get_jwt()

        if id == 'all':
            if jwt_data['role'] != 'admin':
                raise APIException('Access denied', 403)

            return jsonify([x.serialize() for x in Profiles.query.all()]), 200

        if id == 'me':
            id = str(user_id)

        if not id.isnumeric():
            raise APIException('Invalid id: ' + id, 400)

        user = Profiles.query.get(int(id))
        if user is None:
            raise APIException('Profile not found', 404)

        return jsonify(user.serialize()), 200




    @app.route('/profiles', methods=['POST'])
    @role_jwt_required(['user'])
    def register_profile(user_id):

        prof = Profiles.query.get( user_id )
        if prof is not None:
            raise APIException('A profile already exists with "id": '+user_id, 400)

        req = request.get_json()
        utils.check_params(req, 'first_name', 'last_name', 'device_token')

        db.session.add( Profiles(
            id = user_id,
            first_name = req['first_name'],
            last_name = req['last_name'],
            nickname = req.get('nickname'),
            hendon_url = req.get('hendon_url')
        ))
        db.session.add( Devices(
            user_id = user_id,
            token = req['device_token']
        ))
        db.session.add( Transactions(
            user_id = user_id,
            coins = 5
        ))
        db.session.commit()


        return jsonify({'message':'ok'}), 200

      
      
      
    @app.route('/profiles/me', methods=['PUT'])
    @role_jwt_required(['user'])
    def update_profile(user_id):

        prof = Profiles.query.get(user_id)

        req = request.get_json()
        utils.check_params(req)

        utils.update_table(prof, req, ignore=['profile_pic_url'])

        db.session.commit()

        return jsonify(prof.serialize())




    @app.route('/profiles/image', methods=['PUT'])
    @role_jwt_required(['user'])
    def update_profile_image(user_id):

        user = Users.query.get(user_id)

        if 'image' not in request.files:
            raise APIException('"image" property missing on the files array', 404)

        result = utils.cloudinary_uploader(
            image = request.files['image'],
            public_id = 'profile' + str(user.id),
            tags = ['profile_picture']
        )

        user.profile.profile_pic_url = result['secure_url']

        db.session.commit()

        return jsonify({'profile_pic_url': result['secure_url']}), 200




    @app.route('/me/buy_ins', methods=['GET'])
    @role_jwt_required(['user'])
    def get_buy_in(user_id):
        
        buyin = Buy_ins.query.filter_by(user_id=user_id).order_by(Buy_ins.id.desc()).first()
        if buyin is None:
            raise APIException('Buy_in not found', 404)

        return jsonify(buyin.serialize()), 200




    @app.route('/me/buy_ins/flight/<int:id>/image', methods=['PUT'])
    @role_jwt_required(['user'])
    def update_buyin_image(user_id, id):
        
        close_time = utils.designated_trmnt_close_time()

        flight = Flights.query.get( id )
        if flight is None or flight.start_at < close_time:
            raise APIException(
                "Cannot buy into this flight. It either has ended, or does not exist")

        buyin = Buy_ins(
            user_id = user_id,
            flight_id = id
        )
        db.session.add(buyin)
        db.session.flush()

        if 'image' not in request.files:
            raise APIException('"image" property missing in the files array', 404)
        
        
        utils.resolve_google_credentials()
        
        result = utils.cloudinary_uploader(
            type = 'buyin',
            image = request.files['image'],
            public_id = 'buyin' + str(buyin.id),
            tags = ['buyin_receipt',
                'user_'+ str(user_id),
                'buyin_'+ str(buyin.id)]
        )


        buyin.receipt_img_url = result['secure_url']
        db.session.commit()

        receipt_data = utils.ocr_reading( result )
        if receipt_data is None:
            raise APIException('Take another photo')
        
        return jsonify({
            'buyin_id': buyin.id,
            'receipt_data': regex.hard_rock( receipt_data )
        })

        # if receipt_data['tournament_name'] is None or receipt_data['date'] is None:
        #     raise APIException('Can not read picture, take another', 500)

        # # Validate buyin receipt w tournament name and flight start_at
        # now = datetime.utcnow
        # if (now - buyin.flight.start_at) > timedelta(hours=17) and \
        #     receipt_data['tournament_name'] != buyin.flight.tournament.name:
        
        #     send_email(template='wrong_receipt', emails=buyin.user.user.email,
        #         data={
        #             'receipt_url': buyin.receipt_img_url,
        #             'tournament_date': buyin.flight.tournament.start_at,
        #             'tournament_name': buyin.flight.tournament.name,
        #             'upload_time': result['created_at']
        #         })
        #     raise APIException('Wrong receipt was upload', 400)

        # return jsonify({
        #     'buyin_id': buyin.id,
        #     'ocr_data': {
        #         'player_name': f'{buyin.user.first_name} {buyin.user.last_name}',
        #         'date_on_receipt': '12/03/19',
        #         'buyin_amount': '150.00',
        #         'seat': 8,
        #         'table': 198,
        #         'account_number': '2081669'
        #     }
        # })


        

    @app.route('/me/buy_ins/<int:id>', methods=['PUT'])
    @role_jwt_required(['user'])
    def update_buy_in(user_id, id):

        req = request.get_json()
        utils.check_params(req)

        buyin = Buy_ins.query.get(id)
        if buyin is None:
            raise APIException('Buy_in not found', 404)

        if buyin.status._value_ == 'busted':
            raise APIException('This buyin has a status of "busted"')


        if request.args.get('validate') == 'true' and buyin.status._value_ == 'pending':
            utils.check_params(req, 'chips','table','seat')
            buyin.status = 'active'
            # send_email(template='buyin_receipt', emails=buyin.user.user.email,
                # data={
                #     'receipt_url': buyin.receipt_img_url,
                #     'tournament_date': buyin.flight.tournament.start_at,
                #     'tournament_name': buyin.flight.tournament.name
                # })


        elif buyin.status._value_ == 'pending':
            raise APIException('This buyin has not been validated', 406)

        # Update status
        if req.get('status') == 'busted':
            buyin.status = 'busted'

        # Update chips, table and seat
        if req.get('chips') is not None:
            if req['chips'] > 999999999:
                raise APIException('Too many characters for chips')
            buyin.chips = req['chips']
        if req.get('table') is not None:
            if len( req['table'] ) > 20:
                raise APIException('Too many characters for table')
            buyin.table = req['table']
        if req.get('seat') is not None:
            buyin.seat = req['seat']

        db.session.commit()
        
        return jsonify({'buy_in': buyin.serialize()})




    @app.route('/tournaments/<id>', methods=['GET'])
    @role_jwt_required(['user'])
    def get_tournaments(user_id, id):

        if id == 'all':
            now = datetime.utcnow() - timedelta(days=1)

            # Filter past tournaments
            if request.args.get('history') == 'true':
                trmnts = Tournaments.get_history()

            # Filter current and future tournaments
            else:
                trmnts = Tournaments.get_live_upcoming()
                    
            # Filter by name
            name = request.args.get('name') 
            if name is not None:
                trmnts = trmnts.filter( Tournaments.name.ilike(f'%{name}%') )


            # Order by zip code
            zip = request.args.get('zip', '')
            if zip.isnumeric():
                path = os.environ['APP_PATH']
                with open( path + '/src/zip_codes.json' ) as zip_file:
                    data = json.load(zip_file)
                    zipcode = data.get(zip)
                    if zipcode is None:
                        raise APIException('Zipcode not in file', 500)
                    lat = zipcode['latitude']
                    lon = zipcode['longitude']

            # Order by user location
            else:
                lat = request.args.get('lat', '')
                lon = request.args.get('lon', '')

            if isfloat(lat) and isfloat(lon):
                trmnts = trmnts.order_by( 
                    ( db.func.abs(float(lon) - Tournaments.longitude) + 
                      db.func.abs(float(lat) - Tournaments.latitude) )
                .asc() )

            # Order by ascending date
            elif request.args.get('asc') == 'true':
                trmnts = trmnts.order_by( Tournaments.start_at.asc() )

            # Order by descending date
            elif request.args.get('desc') == 'true':
                trmnts = trmnts.order_by( Tournaments.start_at.desc() )

            
            # Pagination
            offset, limit = utils.resolve_pagination( request.args )
            trmnts = trmnts.offset( offset ).limit( limit )

            
            return jsonify(
                [ actions.swap_tracker_json( trmnt, user_id ) for trmnt in trmnts ]
            ), 200


        # Single tournament by id
        elif id.isnumeric():
            trmnt = Tournaments.query.get(int(id))
            if trmnt is None:
                raise APIException('Tournament not found', 404)

            return jsonify( actions.swap_tracker_json( trmnt, user_id )), 200


        raise APIException('Invalid id', 400)




    @app.route('/me/swaps', methods=['POST'])
    @role_jwt_required(['user'])
    def create_swap(user_id):

        # Get sender user
        sender = Profiles.query.get(user_id)
        
        # Get request json
        req = request.get_json()
        utils.check_params(req, 'tournament_id', 'recipient_id', 'percentage')
        
        if user_id == req['recipient_id']:
            raise APIException( f'Cannot swap with yourself, user_id: {user_id}, '
                                f'recipient_id: {req["recipient_id"]}' )

        # Check for sufficient coins
        swap_cost = req.get('cost', 1)
        if swap_cost < 1:
            raise APIException('No free swaps', 400)
        if sender.get_coins() - sender.get_reserved_coins() < swap_cost:
            raise APIException('Insufficient coins to make this swap', 402)
        

        # Get recipient user
        recipient = Profiles.query.get( req['recipient_id'] )
        if recipient is None:
            raise APIException('Recipient user not found', 404)

        # Check recipient swap availability
        if recipient.swap_availability_status._value_ == 'unavailable':
            raise APIException('This person is unavailable for swaps', 401)


        # Can only send one swap offer at a time
        existing_swaps = Swaps.query.filter_by(
            sender_id = user_id,
            recipient_id = recipient.id,
            tournament_id = req['tournament_id']
        )
        unacceptable_status = ['pending','incoming','counter_incoming']
        for swap in existing_swaps:
            if swap.status._value_ in unacceptable_status:
                raise APIException(
                    f'Already have a swap with status "{swap.status._value_}" with this player', 401 )


        percentage = req['percentage']
        counter = req.get('counter_percentage', percentage)
        if percentage < 1 or counter < 1:
            raise APIException('Cannot swap less than %1', 400)

        # Check tournament existance
        trmnt = Tournaments.query.get( req['tournament_id'] )
        if trmnt is None:
            raise APIException('Tournament not found', 404)


        # Swap percentage availability
        sender_availability = sender.available_percentage( req['tournament_id'] )
        if percentage > sender_availability:
            raise APIException(('Swap percentage too large. You can not exceed 50% per tournament. '
                                f'You have available: {sender_availability}%'), 400)

        recipient_availability = recipient.available_percentage( req['tournament_id'] )
        if counter > recipient_availability:
            raise APIException(('Swap percentage too large for recipient. '
                                f'He has available to swap: {recipient_availability}%'), 400)


        swap = Swaps(
            sender_id = user_id,
            tournament_id = req['tournament_id'],
            recipient_id = recipient.id,
            percentage = percentage,
            cost = swap_cost,
            status = 'pending' )
        counter_swap = Swaps(
            sender_id = recipient.id,
            tournament_id = req['tournament_id'],
            recipient_id = user_id,
            percentage = counter,
            cost = swap_cost,
            status = 'incoming',
            counter_swap = swap )
        swap.counter_swap = counter_swap

        db.session.add_all([ swap, counter_swap ])
        db.session.commit()

        # send_fcm('swap_incoming_notification', recipient.id)
        return jsonify({'message':'Swap created successfully.'}), 200




    @app.route('/me/swaps/<int:id>', methods=['PUT'])
    @role_jwt_required(['user'])
    def update_swap(user_id, id):

        # Get sender user
        sender = Profiles.query.get(user_id)

        req = request.get_json()
        utils.check_params(req)
        

        # Get swaps
        swap = Swaps.query.get(id)
        if sender.id != swap.sender_id:
            raise APIException('Access denied: You are not the sender of this swap', 401)
        current_percentage = swap.percentage
        if sender.get_coins() < swap.cost:
            raise APIException('Insufficient coins to see this swap', 402)

        if swap.status._value_ in ['canceled','rejected','agreed']:
            raise APIException('This swap can not be modified', 400)

        counter_swap_body = {}
        counter_swap = Swaps.query.get( swap.counter_swap_id )
        if swap is None or counter_swap is None:
            raise APIException('Swap not found', 404)


        # Get recipient user
        recipient = Profiles.query.get( swap.recipient_id )
        if recipient is None:
            raise APIException('Recipient user not found', 404)
 

        new_status = req.get('status')
        current_status = swap.status._value_

        if 'percentage' in req and new_status not in ['agreed','rejected','canceled']:

            percentage = req['percentage']
            counter = req.get('counter_percentage', percentage)
            if percentage < 1 or counter < 1:
                raise APIException('Cannot swap less than %1', 400)

            sender_availability = sender.available_percentage( swap.tournament_id )
            considering_this_swap = current_status == 'incoming'
            actions = percentage if considering_this_swap else (percentage - swap.percentage)
            if actions > sender_availability:
                raise APIException(('Swap percentage too large. You can not exceed 50% per tournament. '
                                    f'You have available: {sender_availability}%'), 400)

            recipient_availability = \
                recipient.available_percentage( swap.tournament_id )
            if (counter - counter_swap.percentage) > recipient_availability:
                raise APIException(('Swap percentage too large for recipient. '
                                    f'He has available to swap: {recipient_availability}%'), 400)

            # Update percentages
            swap.percentage = percentage
            counter_swap.percentage = counter


        if current_status == 'pending':
            if new_status == 'agreed':
                raise APIException('Cannot agree a swap on a pending status', 400)
            if new_status == 'rejected':
                raise APIException('Cannot reject this swap', 400)
        if current_status in ['incoming','counter_incoming'] and new_status == 'canceled':
            raise APIException('Cannot cancel this swap', 400)
        
        # Update status
        if new_status in ['agreed','rejected','canceled']:
            if new_status == 'agreed':
                if recipient.get_coins() < swap.cost:
                    raise APIException('Recipient has insufficient coins to process this swap')
                if current_status == 'incoming':
                    overdraft = current_percentage - sender.available_percentage( swap.tournament_id )
                    if overdraft > 0:
                        raise APIException(
                            f'Cannot agree to this swap, you are overdrafting by {str(overdraft)}%', 400)
            swap.status = new_status
            counter_swap.status = Swaps.counter_status( new_status )
        # If current swap is pending, leave statuses as they are
        elif current_status != 'pending':
            swap.status = Swaps.counter_status( swap.status._value_ )
            counter_swap.status = Swaps.counter_status( counter_swap.status._value_ )
            # send_fcm('swap_incoming_notification', recipient.id)


        db.session.commit()


        if new_status == 'agreed':

            db.session.add( Transactions(
                user_id = user_id,
                coins = -swap.cost
            ))
            db.session.add( Transactions(
                user_id = recipient.id,
                coins = -swap.cost
            ))
            db.session.commit()

            # send_fcm('swap_agreed_notificatin', recipient.id)
            user1_receipt = Buy_ins.get_latest(sender.id, swap.tournament_id)
            user2_receipt = Buy_ins.get_latest(recipient.id, swap.tournament_id)
            
            send_email( template='swap_confirmation', emails=[sender.user.email, recipient.user.email],
                data={
                    'tournament_date': swap.tournament.start_at,
                    'tournament_name': swap.tournament.name,
                    
                    'user1_name': f'{sender.first_name} {sender.last_name}',
                    'user1_prof_pic': sender.profile_pic_url,
                    'user1_percentage': swap.percentage,
                    'user1_receipt_url': user1_receipt and user1_receipt.receipt_img_url,

                    'user2_name': f'{recipient.first_name} {recipient.last_name}',
                    'user2_prof_pic': recipient.profile_pic_url,
                    'user2_percentage': counter_swap.percentage,
                    'user2_receipt_url': user2_receipt and user2_receipt.receipt_img_url
                })


        return jsonify([
            swap.serialize(),
            counter_swap.serialize(),
        ])




    @app.route('/swaps/me/tournament/<int:id>', methods=['GET'])
    @role_jwt_required(['user'])
    def get_swaps_actions(user_id, id):

        prof = Profiles.query.get(user_id)

        return jsonify(prof.get_swaps_actions(id))




    @app.route('/users/me/swaps/<int:id>/done', methods=['PUT'])
    @role_jwt_required(['user'])
    def set_swap_paid(user_id, id):

        sender = Profiles.query.get(user_id)

        req = request.get_json()
        utils.check_params(req, 'tournament_id', 'recipient_id')

        # Security validation
        swap = Swaps.query.get(id)
        if req['tournament_id'] !=  swap.tournament_id \
            or req['recipient_id'] != swap.recipient_id:
            raise APIException('IDs do not match', 400)

        if swap.status._value_ != 'agreed':
            raise APIException('This swap has not been agreed upon', 400)

        if swap.paid == True:
            raise APIException('This swap is already paid', 400)

        swap.paid = True

        db.session.commit()

        return jsonify({'message':'Swap has been paid'})




    @app.route('/me/swap_tracker', methods=['GET'])
    @role_jwt_required(['user'])
    def swap_tracker(user_id):
        
        if request.args.get('history') == 'true':
            trmnts = Tournaments.get_history(user_id=user_id)
        else:
            trmnts = Tournaments.get_live_upcoming(user_id=user_id)

        swap_trackers = []

        if trmnts is not None:
            
            for trmnt in trmnts:
                json = actions.swap_tracker_json( trmnt, user_id )
                swap_trackers.append( json )

        return jsonify( swap_trackers )




    @app.route('/users/me/transaction', methods=['POST'])
    @role_jwt_required(['user'])
    def add_coins(user_id):

        req = request.get_json()
        utils.check_params(req, 'coins')

        db.session.add( Transactions(
            user_id = user_id,
            coins = req['coins'],
            dollars = req.get('dollars', 0)
        ))

        db.session.commit()

        user = Profiles.query.get( user_id )
        return jsonify({'total_coins': user.get_coins()})




    @app.route('/users/me/transaction/report', methods=['GET'])
    @role_jwt_required(['user'])
    def transaction_report(user_id):
        
        month_ago = datetime.utcnow() - timedelta(months=1)

        report = Transactions.query \
                    .filter( Transaction.created_at > month_ago ) \
                    .order_by( Transactions.created_at.desc() )

        return jsonify([x.serialize() for x in report])



    return app
