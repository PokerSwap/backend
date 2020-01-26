from flask import request, jsonify, render_template
from flask_cors import CORS
from flask_jwt_simple import JWTManager, create_jwt, decode_jwt, get_jwt
from utils import APIException, check_params, jwt_link, update_table, sha256, role_jwt_required
from models import db, Users, Devices
from notifications import send_email

def attach(app):

    @app.route('/users', methods=['POST'])
    def register_user():

        req = request.get_json()
        check_params(req, 'email', 'password')

        # If user exists and failed to validate his account
        user = (Users.query
                .filter_by( email=req['email'], password=sha256(req['password']) )
                .first())

        if user and user.status._value_ == 'invalid':     
            data = {'validation_link': jwt_link(user.id)}
            send_email( template='email_validation', emails=user.email, data=data)
            
            return jsonify({'message':'Another email has been sent for email validation'})

        elif user and user.status._value_ == 'valid':
            raise APIException('User already exists', 405)

        user = Users(
            email = req['email'],
            password = sha256(req['password'])
        )
        db.session.add(user)
        db.session.commit()

        user = Users.query.filter_by(email=req['email']).first()

        send_email( template='email_validation', emails=user.email, 
            data={'validation_link': jwt_link(user.id)} )

        return jsonify({
            'message': 'Please verify your email',
            'validation_link': jwt_link(user.id)
        }), 200




    @app.route('/users/token', methods=['POST'])
    def login():

        req = request.get_json()
        check_params(req, 'email', 'password', 'device_token')

        user = Users.query.filter_by( email=req['email'], password=sha256(req['password']) ).first()

        if user is None:
            raise APIException('User not found', 404)

        if user.status._value_ == 'invalid':
            raise APIException('Email not validated', 405)

        db.session.add( Devices(
            user_id = user.id,
            token = req['device_token']
        ))
        db.session.commit()

        return jsonify({
            'jwt': create_jwt({
                'id': user.id,
                'role': 'user',
                'exp': req.get('exp', 15)
            })
        }), 200




    @app.route('/users/validate/<token>', methods=['GET'])
    def validate(token):

        jwt_data = decode_jwt(token)

        accepted_roles = ['validating','email_change']
        if jwt_data['role'] not in accepted_roles:
            raise APIException('Incorrect token', 400)

        user = Users.query.filter_by(id = jwt_data['sub']).first()
        if user is None:
            raise APIException('Invalid key payload', 400)

        if user.status._value_ == 'invalid':
            user.status = 'valid'
            db.session.commit()

        if jwt_data['role'] == 'validating':
            send_email(template='welcome', emails=user.email)

        return render_template('email_validated_success.html')




    return app
