import os
import re
import hashlib
import cloudinary
import cloudinary.uploader
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
        raise APIException('You must specify the ' + msg, 400)

def update_table(table, body, ignore=[]):
    ignore = [*ignore, 'created_at', 'updated_at']
    for attr, value in body.items():
        if attr not in ignore:
            if not hasattr(table, attr):
                raise APIException(f'Incorrect parameter in body: {attr}', 400)
            setattr(table, attr, value)

def jwt_link(id, path='users/validate/', role='first_time_validation'):
    return os.path.join(
        os.environ['API_HOST'], path, create_jwt({'id':id, 'role':role}) )

def sha256(string):
    m = hashlib.sha256()
    m.update(string.encode('utf-8'))
    return m.hexdigest()

def resolve_pagination(request_args, limit_default=10):
    page = request_args.get('page', '0')
    offset = int(page) - 1 if page.isnumeric() and int(page) > 0 else 0
    
    limit = request_args.get('limit', '10')
    limit = int(limit) if limit.isnumeric() and int(limit) > 0 else limit_default
    
    return offset, limit

def isfloat(string):
    try:
        float(string)
        return True
    except:
        return False

def cloudinary_uploader(image, public_id, tags):
    return cloudinary.uploader.upload(
        image,
        public_id=public_id,
        crop='limit',
        width=450,
        height=450,
        eager=[{
            'width': 200, 'height': 200,
            'crop': 'thumb', 'gravity': 'face',
            'radius': 100
        }],
        tags=tags
    )

# Notes: 'admin' will have access even if arg not passed
def role_jwt_required(valid_roles=['invalid']):
    def decorator(func):

        @jwt_required
        def wrapper(*args, **kwargs):

            jwt_role = get_jwt()['role']
            valid = jwt_role == 'admin'

            for role in valid_roles:
                if role == jwt_role:
                    valid = True

            if not valid:
                raise APIException('Access denied', 403)

            user_id = get_jwt()['sub']
            
            user = Users.query.get(user_id)
            if not user:
                raise APIException('User not found with id: '+str(user_id), 404)
            
            invalid_status = ['suspended','invalid']
            if user.status._value_ in invalid_status:
                raise APIException(f'The user account is "{user.status._value_}"', 403)

            kwargs = {
                **kwargs,
                'user_id': user_id
            }

            return func(*args, **kwargs)

        # change wrapper name so it can be used for more than one function
        wrapper.__name__ = func.__name__

        return wrapper
    return decorator
