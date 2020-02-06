import os
import models
import requests
from flask import Flask, jsonify, request
from notifications import send_email

def attach(app):

    @app.route('/sendemail')
    def sendemailtest():
        msg = {'name':'Hello Hernan'}
        r = send_email('account_suspension','hernanjkd@gmail.com',data=msg)
        
        return str(r)




    @app.route('/testing', methods=['GET'])
    def first_endpoint():
        req = requests.get('http://localhost:3333/roi/data/asd');return req.text
        d = dir(req)
        class_info = { 'attributes': {attr: str(val) for attr, val in req.__dict__.items()} }
        class_info['methods'] = [method for method in d if method not in class_info['attributes']]
        return jsonify( class_info )
        
        trmnts = models.Tournaments.query.all()
        lst = []
        for t in trmnts:
            data = requests.get('http://localhost:3333/zipcode/' + str(t.zip_code)).json()
            if data:
                lst = [*lst, data]
                # t.longitude = data.longitude
                # t.latitude = data.latitude
                # models.db.session.commit()
        return jsonify(lst)
        return jsonify({ 'details': 'All good my friend'}), 200


    @app.route('/mailgun')
    def get_logs():
        return jsonify( requests.get(
            f"https://api.mailgun.net/v3/{os.environ.get('MAILGUN_DOMAIN')}/events",
            auth=("api", os.environ.get("MAILGUN_API_KEY")),
            params={"begin"       : "Fri, 13 DEC 2019 09:00:00 -0000",
                    "ascending"   : "yes",
                    "limit"       :  25,
                    "pretty"      : "yes",
                    "recipient" : "hernanjkd@gmail.com"}).json())

    @app.route('/ocr_image', methods=['PUT'])
    def ocr():
        import cloudinary
        import cloudinary.uploader
        from google.cloud import vision


        result = cloudinary.uploader.upload(
            request.files['image'],
            public_id='ocr',
            crop='limit',
            width=450,
            height=450,
            eager=[{
                'width': 200, 'height': 200,
                'crop': 'thumb', 'gravity': 'face',
                'radius': 100
            }],
            tags=[
                'buyin_receipt',
                f'user_',
                f'buyin_'
            ]
        )
        
        client = vision.ImageAnnotatorClient()
        image = vision.types.Image()
        image.source.image_uri = result['secure_url']

        response = client.text_detection(image=image)
        texts = response.text_annotations
        msg = texts[0].description
        
        cloudinary.uploader.destroy('ocr')
        
        buyin = re.search(r'buy[\s\-_]*in\D{1,5}([0-9,\.]+)', msg, re.IGNORECASE)
        buyin = buyin and buyin.group(1)
        seat = re.search(r'seat\D{,5}([0-9]+)', msg, re.IGNORECASE)
        seat = seat and seat.group(1)
        table = re.search(r'table\D{,5}([0-9]+)', msg, re.IGNORECASE)
        table = table and table.group(1)
        name = re.search(r'name[ :,]+([a-zA-Z() ]+)', msg, re.IGNORECASE)
        name = name and name.group(1)
        # user id for that casino

        return jsonify({
            'text': msg,
            'buy_in': buyin,
            'seat': seat,
            'table': table,
            'name': name
        })

    return app