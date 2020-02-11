import pytest
from flask_jwt_simple import decode_jwt, create_jwt

def test_correct_signup(client):

    resp = client.post('/create/token')
    assert resp.status_code == 200, "I should be able to create a token"

    decoded_data = decode_jwt(resp.data.decode().strip('"'))
    assert 'exp' in decoded_data, "The decoded data must have expiration"

def test_incorrect_email_validation(client):

    token = create_jwt("sdasdads")

    resp = client.get('/users/validate/'+token)
    assert resp.status_code == 400, "I'm encoding with the wrong seed"

def test_wrong_jwt_payload_email_validation(client):

    token = create_jwt({
        "role": "first_time_validation"
    })

    resp = client.get('/users/validate/'+token)
    assert resp.status_code == 400, "Its missing required keys like 'sub'"

def test_correct_email_validation(client):

    token = create_jwt({
        "sub": 1,
        "role": "first_time_validation"
    })

    resp = client.get('/users/validate/'+token)
    assert resp.status_code == 200, "I should be able to create a token"