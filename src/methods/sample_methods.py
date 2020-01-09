from flask import Flask, jsonify, request
from notifications import send_email
import requests
import os
import models

def attach(app):

    @app.route('/sendemail')
    def sendemailtest():
        msg = {'name':'Hello Hernan'}
        r = send_email('account_suspension','hernanjkd@gmail.com',data=msg)
        
        return str(r)




    @app.route('/testing', methods=['GET'])
    def first_endpoint():
        
        return jsonify( requests.get('http://localhost:3333/zipcode/89145').json() )

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

        # return cloudinary.uploader.destroy('ocr')

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
        cloudinary.uploader.destroy('ocr')
        return jsonify(result)
        client = vision.ImageAnnotatorClient()
        image = vision.types.Image()
        image.source.image_uri = result['secure_url']

        response = client.text_detection(image=image)
        texts = response.text_annotations

        cloudinary.uploader.destroy('ocr')
        return jsonify(texts[0].description)

    return app