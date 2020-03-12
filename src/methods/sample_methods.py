import os
import utils
import models
import requests
from flask import Flask, jsonify, request
from notifications import send_email, send_fcm

def attach(app):

    @app.route('/sendemail')
    def sendemailtest():
        msg = {'name':'Hello Hernan'}
        r = send_email('account_suspension','hernanjkd@gmail.com',data=msg)
        
        return str(r)


    @app.route('/sendfcm/<device_token>')
    def sendfcmtest(device_token):
        utils.resolve_google_credentials()
        return send_fcm(0,0,
            data={
                "token": device_token,
                "title": "A Tournament Went Live!",
                "body": "The Alamo Hold'em 2019 tournament is now live",
                "data" : {
                    "type": "tournament",
                    "id": "3",
                    "initialPath": "Tournaments",
                    "finalPath": "TourneyLobby"
                }
            }
        )


    @app.route('/testing', methods=['GET'])
    def first_endpoint():
        import os
        return jsonify( 
            [x.start_at for x in models.Tournaments.query \
                .filter_by(name='Hialeah - $50,000 Guaranteed').first().flights] )


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
        import re
        import os

        utils.resolve_google_credentials()
        
        result = utils.cloudinary_uploader( 'buyin',
            request.files['image'], 'ocr', 
            ['buyin_receipt',f'user_',f'buyin_'] )
        
        msg = utils.ocr_reading( result )
        
        import regex
        r = regex.hard_rock(msg)

        return jsonify({ **r, 'text': msg })

    return app