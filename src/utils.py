import os
import re
import hashlib
import cloudinary
import cloudinary.uploader
from google.cloud import vision
from flask import jsonify, url_for
from flask_jwt_simple import create_jwt, jwt_required, get_jwt
from datetime import datetime, timedelta
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

def resolve_name_day(string):
    a = re.search(r'(.*) - Day ([\d\w]+)', string)
    tournament_name = string if a is None else a.group(1)
    flight_day = a and a.group(2)
    return [tournament_name, flight_day]

def resolve_google_credentials():
    path = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
    if not os.path.exists( path ):
        credentials = os.environ['GOOGLE_CREDENTIALS'].replace("\\\\","\\")
        with open(path, 'w') as credentials_file:
            credentials_file.write( credentials )

def isfloat(string):
    try:
        float(string)
        return True
    except: return False

def designated_trmnt_close_time():
    return datetime.utcnow() - timedelta(hours=17, minutes=1)

def cloudinary_uploader(type, image, public_id, tags):
    return cloudinary.uploader.upload(
        image,
        public_id=public_id,
        crop='limit',
        width=450 if type == 'profile' else 1000,
        height=450 if type == 'profile' else 1000,
        eager=[{
            'width': 200, 'height': 200,
            'crop': 'thumb', 'gravity': 'face',
            'radius': 100
        }] if type == 'profile' else None,
        tags=tags
    )

def ocr_reading(result):
    client = vision.ImageAnnotatorClient()
    image = vision.types.Image()
    image.source.image_uri = result['secure_url']

    response = client.text_detection(image=image)
    texts = response.text_annotations
    return texts and texts[0].description

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

# Put in at the end of POST /swaps and PUT /swaps for debugging
'''
log = {
    '1 sender id': sender.id,
    '2 before availability': sender_availability,
    '3 after availability': sender.available_percentage( swap.tournament_id ),
    '4 swap id': swap.id,
    '5 swap status': swap.status._value_,
    '6 actions': sender.get_swaps_actions( swap.tournament_id ),
    '7 recipient id': recipient.id,
    '8 before availability': recipient_availability,
    '9 after availability': recipient.available_percentage( swap.tournament_id ),
    'a swap id': counter_swap.id,
    'b swap status': counter_swap.status._value_,
    'c recipient swap actions': recipient.get_swaps_actions( swap.tournament_id )
}
'''