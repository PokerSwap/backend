import os
import re
import hashlib
from flask import jsonify, url_for
from flask_jwt_simple import create_jwt, jwt_required, get_jwt
from datetime import datetime
from models import Users

class APIException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

# Raises an exception if required params not in body
def check_params(body, *args):
    msg = ''
    if body is None:
        msg = 'request body as a json object, '
    else:
        for prop in args:
            if prop not in body:
                msg += f'{prop}, '
    if msg:
        msg = re.sub(r'(.*),', r'\1 and', msg[:-2])
        raise Exception('You must specify the ' + msg, 400)

def update_table(table, body, ignore=[]):
    for attr, value in body.items():
        if attr not in ignore:
            if not hasattr(table, attr):
                raise Exception(f'Incorrect parameter in body: {attr}', 400)
            setattr(table, attr, value)

def validation_link(id):
    return os.environ.get('API_HOST') + '/users/validate/' + create_jwt({'id':id, 'role':'validating'})

def sha256(string):
    m = hashlib.sha256()
    m.update(string.encode('utf-8'))
    return m.hexdigest()

# Notes: 'admin' will have access even if arg not passed
def role_jwt_required(valid_roles=['invalid']):
    def decorator(func):

        @jwt_required
        def wrapper(*args, **kwargs):

            jwt_role = get_jwt()['role']
            valid = True if jwt_role == 'admin' else False

            for role in valid_roles:
                if role == jwt_role:
                    valid = True

            if not valid:
                raise Exception('Access denied', 401)

            user_id = get_jwt()['sub']
            if not Users.query.get(user_id):
                raise Exception('User not found', 404)

            kwargs = {
                **kwargs,
                'user_id': user_id
            }

            return func(*args, **kwargs)

        # change wrapper name so it can be used for more than one function
        wrapper.__name__ = func.__name__

        return wrapper
    return decorator
