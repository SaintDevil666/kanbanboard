from flask import Blueprint, request, g
import string
import secrets
import hashlib
import uuid
import datetime

from db import get_db
from utils import auth_required, json_response, is_valid_email, encrypt_password, verify_password

user_bp = Blueprint('user', __name__)


@user_bp.route('/register', methods=['POST'])
def register():
    body = request.json
    
    if not body:
        return json_response({'error': 'Невизначене тіло запиту'}, 400)
    
    if 'name' not in body or not (type(body['name']) is str) or not body['name'].strip():
        return json_response({'error': 'Некоректне значення: name'}, 400)
    if 'email' not in body or not (type(body['email']) is str) or not is_valid_email(body['email']):
        return json_response({'error': 'Некоректне значення: email'}, 400)
    if 'password' not in body or not (type(body['password']) is str) or not len(body['password']) >= 6:
        return json_response({'error': 'Некоректне значення: password'}, 400)

    name = body['name']
    email = body['email']
    password = body['password']
    db = get_db()
    
    existing_user = db.Users.find_one({'email': email})
    if existing_user:
        return json_response({'error': 'Користувач з такою поштою вже існує!'}, 400)

    (hashed_password, salt) = encrypt_password(password)

    user = {
        'name': name,
        'email': email,
        'password': hashed_password,
        'salt': salt,
        'joinedAt': datetime.datetime.now(),
        'settings': {
            'defaultStatuses': [
                { "name": "To Do", "color": "black.PNG" },
                { "name": "В роботі", "color": "cyan.PNG" },
                { "name": "Виконано", "color": "gray.PNG" }
            ]
        }
    }
    result = db.Users.insert_one(user)

    token = str(uuid.uuid4())
    
    db.Tokens.insert_one({
        'userID': result.inserted_id,
        'token': token
    })
    
    return json_response({'token': token}, 201)


@user_bp.route('/login', methods=['POST'])
def login():
    body = request.json
    
    if not body:
        return json_response({'error': 'Невизначене тіло запиту'}, 400)
    
    if 'email' not in body or not (type(body['email']) is str) or not is_valid_email(body['email']):
        return json_response({'error': 'Некоректне значення: email'}, 400)
    if 'password' not in body or not (type(body['password']) is str):
        return json_response({'error': 'Некоректне значення: password'}, 400)
    
    email = body['email']
    password = body['password']

    db = get_db()
    
    user = db.Users.find_one({'email': email})
    if not user:
        return json_response({'error': 'Неправильна пошта або пароль'}, 400)
    
    if not verify_password(password, user['password'], user['salt']):
        return json_response({'error': 'Неправильна пошта або пароль'}, 400)
    
    token = str(uuid.uuid4())
    
    db.Tokens.insert_one({
        'userID': user['_id'],
        'token': token
    })
    
    return json_response({'token': token})


@user_bp.route('/logout', methods=['POST'])
@auth_required
def logout():
    token = request.headers['Authorization'].split(' ')[1]
    
    db = get_db()
    db.Tokens.delete_one({'token': token})
    
    return json_response()


@user_bp.route('/profile', methods=['GET'])
@auth_required
def get_profile():
    profile = {
        'id': str(g.user['_id']),
        'name': g.user['name'],
        'email': g.user['email'],
        'settings': g.user['settings']
    }
    
    return json_response(profile)


@user_bp.route('/profile', methods=['PATCH'])
@auth_required
def update_profile():
    body = request.json
    
    if not body:
        return json_response({'error': 'Невизначене тіло запиту'})
    
    if 'name' in body and (not (type(body['name']) is str) or not body['name'].strip()):
        return json_response({'error': 'Некоректне значення: name'}, 400)
    if 'email' in body and (not (type(body['email']) is str) or not is_valid_email(body['email'])):
        return json_response({'error': 'Некоректне значення: email'}, 400)
    if 'password' in body and (not 'currentPassword' in body or not (type(body['currentPassword']) is str) or not (type(body['password']) is str) or not len(password) >= 6):
        return json_response({'error': 'Некоректне значення: password'}, 400)
    
    db = get_db()
    
    update_data = {}
    
    if 'name' in body:
        update_data['name'] = body['name']
    
    if 'email' in body:
        email = body['email']

        existing_user = db.users.find_one({'_id': {'$ne': g.user['_id']}, 'email': email})
        if existing_user:
            return json_response({'error': 'Користувач з такою поштою вже існує!'}, 400)
        
        update_data['email'] = email
    
    if 'password' in body:
        # validate current password
        salt = g.user['salt']
        if not verify_password(body['currentPassword'], g.user['password'], g.user['salt']):
            return json_response({'error': 'Неправильний поточний пароль користувача'}, 400)
        
        (hashed_password, salt) = encrypt_password(body['password'])
    
        update_data['password'] = hashed_password
        update_data['salt'] = salt

    if 'settings' in body and 'defaultStatuses' in body['settings']:
        default_statuses = body['settings']['defaultStatuses']
        
        if not isinstance(default_statuses, list):
            return json_response({'message': 'Invalid defaultStatuses format'}, 400)

        for status in default_statuses:
            if not isinstance(status, dict) or not isinstance(status.get('name'), str) or not isinstance(status.get('color'), str):
                return json_response({'message': 'Invalid status'}, 400)
        print(default_statuses)
        update_data['settings.defaultStatuses'] = default_statuses
    
    if update_data:
        db.Users.update_one({'_id': g.user['_id']}, {'$set': update_data})
    
    return json_response({'message': 'Профіль успішно оновлено'})