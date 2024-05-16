import string
import secrets
import hashlib
from flask import g, request, jsonify, make_response
from functools import wraps
from bson import ObjectId
import re
from db import get_db

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers.get('Authorization', '')
            auth_parts = auth_header.split(' ')
            if len(auth_parts) == 2 and auth_parts[0] == 'Bearer':
                token = auth_parts[1]
        
        if not token:
            return json_response({'error': 'Unauthorized'}, 401)
        
        db = get_db()
        user_token = db.Tokens.find_one({'token': token})
        if not user_token:
            return json_response({'error': 'Unauthorized'}, 401)
        
        user = db.Users.find_one({'_id': user_token['userID']})
        if not user:
            return json_response({'error': 'Unauthorized'}, 401)
        
        g.user = user
        return f(*args, **kwargs)
    
    return decorated


def encrypt_password(password):
    salt = ''.join(secrets.choice(string.printable) for _ in range(32))

    hash_object = hashlib.sha256()
    hash_object.update((salt+password).encode())
    hashed_password = hash_object.hexdigest()

    return (hashed_password, salt)


def verify_password(attempt, password, salt):
    hash_object = hashlib.sha256()
    hash_object.update((salt+attempt).encode())
    hashed_password = hash_object.hexdigest()

    return hashed_password == password


def json_response(data="", status_code=200):
    if isinstance(data, list):
        data = [convert_to_json(item) for item in data]
    elif isinstance(data, dict):
        data = convert_to_json(data)
    
    response = make_response(jsonify(data), status_code)
    response.headers['Content-Type'] = 'application/json'
    return response


def convert_to_json(data):
    if isinstance(data, ObjectId):
        return str(data)
    elif isinstance(data, list):
        return [convert_to_json(item) for item in data]
    elif isinstance(data, dict):
        return {k: convert_to_json(v) for k, v in data.items()}
    else:
        return data


def is_valid_email(email):
    email_regex = re.compile(r'^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$')
    return email_regex.match(email) is not None