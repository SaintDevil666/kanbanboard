from flask import Blueprint, request, g
from bson import ObjectId
import datetime

from db import get_db
from utils import auth_required, json_response, is_valid_email

boards_bp = Blueprint('boards', __name__)


@boards_bp.route('', methods=['GET'])
@auth_required
def get_boards():
    db = get_db()
    
    boards = list(db.Boards.find({'$or': [{'creatorID': g.user['_id']}, {'invited': g.user['_id']}]}).sort('updatedAt', -1))
    
    for board in boards:
        board['id'] = str(board['_id'])
        del board['_id']
        
        creator = db.Users.find_one({'_id': board['creatorID']})
        board['creator'] = {
            'id': str(creator['_id']),
            'name': creator['name'],
            'email': creator['email']
        }
        del board['creatorID']
    
    return json_response(boards)


@boards_bp.route('', methods=['POST'])
@auth_required
def create_board():
    data = request.json
    
    title = data.get('title', 'Дошка без назви').strip()
    description = data.get('description', '').strip()
    statuses = data.get('statuses', g.user.get('settings', {}).get('defaultStatuses', [{ "name": "To Do", "color": "#FF0000" }, { "name": "В роботі", "color": "#0000FF" }, { "name": "Виконано", "color": "#00FF00" }]))
    
    if not isinstance(statuses, list):
        return json_response({'message': 'Invalid statuses format'}, 400)
    
    for status in statuses:
        if not isinstance(status, dict) or not isinstance(status.get('name'), str) or not isinstance(status.get('color'), str):
            return json_response({'message': 'Invalid status'}, 400)

    if not statuses:
        user_settings = g.user.get('settings', {})
        statuses = user_settings.get('defaultStatuses', [{ "name": "To Do", "color": "#FF0000" }, { "name": "В роботі", "color": "#0000FF" }, { "name": "Виконано", "color": "#00FF00" }])
    
    now = datetime.datetime.now()
    
    board = {
        'title': title,
        'description': description,
        'statuses': statuses,
        'creatorID': g.user['_id'],
        'publicAccess': False,
        'invited': [],
        'createdAt': now,
        'updatedAt': now
    }
    
    db = get_db()
    result = db.Boards.insert_one(board)
    
    board['id'] = str(result.inserted_id)
    board['cards'] = []
    
    return json_response({'id': board['id']}, 201)


@boards_bp.route('/<string:board_id_or_date>', methods=['GET'])
@auth_required
def get_board(board_id_or_date):
    db = get_db()
    
    created_new = False
    if len(board_id_or_date) == 10:  # date format: YYYY-MM-DD
        date = datetime.datetime.strptime(board_id_or_date, '%Y-%m-%d')
        board = db.Boards.find_one({'creatorID': g.user['_id'], 'date': date.strftime('%Y-%m-%d')})
        
        if not board:
            board = {
                'title': '',
                'description': '',
                'statuses': g.user.get('settings', {}).get('defaultStatuses', [{ "name": "To Do", "color": "#FF0000" }, { "name": "В роботі", "color": "#0000FF" }, { "name": "Виконано", "color": "#00FF00" }]),
                'creatorID': g.user['_id'],
                'publicAccess': False,
                'invited': [],
                'date': date.strftime('%Y-%m-%d'),
                'createdAt': datetime.datetime.now(),
                'updatedAt': datetime.datetime.now()
            }
            result = db.Boards.insert_one(board)
            board['_id'] = result.inserted_id
            created_new = True
    else:
        if ObjectId.is_valid(board_id_or_date):
            board_id = ObjectId(board_id_or_date)
        else:
            return json_response({'message': 'Invalid board ID'}, 400)
        
        board = db.Boards.find_one({'_id': board_id, '$or': [{'creatorID': g.user['_id']}, {'invited': g.user['_id']}, {'publicAccess': True}]})
    
    if not board:
        return json_response({'message': 'Board not found'}, 404)

    cards = list(db.Cards.find({'boardID': board['_id']}))
    card_ids = [card['_id'] for card in cards]
    uploads = list(db.Uploads.find({'cardID': {'$in': card_ids}}, {'cardID': {'$toString': '$cardID'}, 'id': {'$toString': '$_id'}, 'name': '$filename'}))

    for card in cards:
        card['id'] = str(card.pop('_id'))
        card['attachments'] = [{'filename': upload['name'], 'fileID': upload['id']} for upload in uploads if upload['cardID'] == card['id']]
        del card['boardID']

    board['cards'] = cards
    board['id'] = str(board.pop('_id'))
    
    creator = db.Users.find_one({'_id': board['creatorID']})
    board['creator'] = {
        'id': str(creator['_id']),
        'name': creator['name'],
        'email': creator['email']
    }
    del board['creatorID']
    
    if str(g.user['_id']) != str(creator['_id']):
        del board['publicAccess']
        del board['invited']
    else:
        for index, invited in enumerate(board['invited']):
            user = db.Users.find_one({"_id": ObjectId(invited)})
            board['invited'][index] = {
                'id': str(user['_id']),
                'name': user['name'],
                'email': user['email']
            }
    
    
    return json_response(board, 201 if created_new else 200)


@boards_bp.route('/<string:board_id>/info', methods=['PATCH'])
@auth_required
def update_board_info(board_id):
    data = request.json
    
    if not data:
        return json_response({'message': 'No data provided'}, 400)
    
    db = get_db()
    
    if ObjectId.is_valid(board_id):
        board_id = ObjectId(board_id)
    else:
        return json_response({'message': 'Invalid board ID'}, 400)
    
    board = db.Boards.find_one({'_id': board_id, '$or': [{'publicAccess': True}, {'creatorID': g.user['_id']}, {'invited': g.user['_id']}, {'publicAccess': True}]})
    
    if not board:
        return json_response({'message': 'Board not found'}, 404)
    
    title = data.get('title', '').strip()
    description = data.get('description', '').strip()
    
    update_data = {}
    
    if title:
        update_data['title'] = title
    
    if description:
        update_data['description'] = description
    
    if update_data:
        update_data['updatedAt'] = datetime.datetime.now()
        db.Boards.update_one({'_id': board_id}, {'$set': update_data})
    
    return json_response()


@boards_bp.route('/<string:board_id>/status', methods=['PATCH'])
@auth_required
def update_board_statuses(board_id):
    data = request.json
    if not data:
        return json_response({'message': 'No data provided'}, 400)

    db = get_db()

    try:
        board_id = ObjectId(board_id)
    except:
        return json_response({'message': 'Invalid board ID'}, 400)

    board = db.Boards.find_one({'_id': board_id, '$or': [{'publicAccess': True}, {'creatorID': g.user['_id']}, {'invited': g.user['_id']}]})

    if not board:
        return json_response({'message': 'Board not found or insufficient permissions'}, 404)

    action = data.get('action')
    if not action:
        return json_response({'message': 'Missing action field'}, 400)

    if action not in ['delete', 'modify', 'add', 'order']:
        return json_response({'message': 'Invalid action'}, 400)

    statuses = board['statuses']

    status_name = data.get('statusName', '').strip()
    if not status_name:
        return json_response({'message': 'Missing statusName field'}, 400)
    
    if action == 'delete':
        status_index = next((index for index, status in enumerate(statuses) if status['name'] == status_name), -1)
        if status_index == -1:
            return json_response({'message': 'Status not found'}, 404)
        
        if len(statuses) == 1:
            return json_response({'message': 'Cannot delete the last status'}, 400)
        
        del statuses[status_index]
        db.Cards.delete_many({'boardID': board_id, 'status': status_name})

    elif action == 'modify':
        to_status_name = data.get('toStatusName', '')
        to_status_color = data.get('toStatusColor', '')
        
        if not to_status_name and not to_status_color:
            return json_response({'message': 'Missing toStatusName and toStatusColor fields'}, 400)
        
        status = next((status for status in statuses if status['name'] == status_name), None)
        if not status:
            return json_response({'message': 'Status not found'}, 404)
        
        if to_status_name:
            status['name'] = to_status_name
            db.Cards.update_many({'boardID': board_id, 'status': status_name}, {'$set': {'status': to_status_name}})
        if to_status_color:
            status['color'] = to_status_color

    elif action == 'add':
        status_color = data.get('statusColor', '')
        
        if not status_color:
            return json_response({'message': 'Missing statusColor field'}, 400)
        
        if any(status['name'] == status_name for status in statuses):
            return json_response({'message': 'Status already exists'}, 400)
        
        statuses.append({'name': status_name, 'color': status_color})

    elif action == 'order':        
        index = data.get('index')
        if index is None or not isinstance(index, int) or index < 0 or index >= len(statuses):
            return json_response({'message': 'Invalid index'}, 400)
        
        status_index = next((index for index, status in enumerate(statuses) if status['name'] == status_name), -1)
        if status_index == -1:
            return json_response({'message': 'Status not found'}, 404)
        
        status = statuses.pop(status_index)
        statuses.insert(index, status)

    db.Boards.update_one({'_id': board_id}, {'$set': {'statuses': statuses, 'updatedAt': datetime.datetime.now()}})

    return json_response()


@boards_bp.route('/<string:board_id>/cards', methods=['PATCH'])
@auth_required
def update_board_cards(board_id):
    data = request.json

    if not data:
        return json_response({'message': 'No data provided'}, 400)

    db = get_db()

    if ObjectId.is_valid(board_id):
        board_id = ObjectId(board_id)
    else:
        return json_response({'message': 'Invalid board ID'}, 400)

    board = db.Boards.find_one({'_id': board_id, '$or': [{'creatorID': g.user['_id']}, {'invited': g.user['_id']}, {'publicAccess': True}]})

    if not board:
        return json_response({'message': 'Board not found'}, 404)

    action = data.get('action')
    
    if not action or action not in ['add', 'update', 'delete']:
        return json_response({'message': 'Missing or invalid action field'}, 400)

    now = datetime.datetime.now()

    card = data.get('card')
    if not card:
        return json_response({'message': 'Missing card data'}, 400)

    resp = {}
    if action == 'add':
        card = {
            'boardID': board_id,
            'status': card.get('status', board['statuses'][0]['name']),
            'title': card.get('title', ''),
            'description': card.get('description', ''),
            'tags': card.get('tags', []),
            'order': card.get('order', 0)
        }
        result = db.Cards.insert_one(card)

        resp['cardId'] = result.inserted_id
    elif action == 'update':
        card_id = card.get('id')
        if not card_id:
            return json_response({'message': 'Missing card ID'}, 400)
        
        update_data = {}
        if 'status' in card:
            update_data['status'] = card['status']
        if 'title' in card:
            update_data['title'] = card['title']
        if 'description' in card:
            update_data['description'] = card['description']
        if 'tags' in card:
            update_data['tags'] = card['tags']

        if update_data:
            db.Cards.update_one({'_id': ObjectId(card_id)}, {'$set': update_data})
    elif action == 'delete':
        card_id = card.get('id')
        if not card_id or not ObjectId.is_valid(card_id):
            return json_response({'message': 'Invalid card ID'}, 400)
        
        db.Cards.delete_one({'_id': ObjectId(card_id)})
        db.Uploads.delete_many({'cardID': ObjectId(card_id)})        

    db.Boards.update_one({'_id': board_id}, {'$set': {'updatedAt': now}})

    return json_response(resp)


@boards_bp.route('/<string:board_id>/publicAccess', methods=['PATCH'])
@auth_required
def update_board_public_access(board_id):
    data = request.json
    
    if not data:
        return json_response({'message': 'No data provided'}, 400)
    
    db = get_db()
    
    try:
        board_id = ObjectId(board_id)
    except:
        return json_response({'message': 'Invalid board ID'}, 400)
    
    board = db.Boards.find_one({'_id': board_id, 'creatorID': g.user['_id']})
    
    if not board:
        return json_response({'message': 'Board not found or insufficient permissions'}, 404)
    
    access = data.get('access')
    
    if access is None or not isinstance(access, bool):
        return json_response({'message': 'Invalid access value'}, 400)
    
    db.Boards.update_one({'_id': board_id}, {'$set': {'publicAccess': access, 'updatedAt': datetime.datetime.now()}})
    
    return json_response()


@boards_bp.route('/<string:board_id>/invite', methods=['POST'])
@auth_required
def invite_user_to_board(board_id):
    data = request.json
    
    if not data:
        return json_response({'message': 'No data provided'}, 400)
    
    db = get_db()
    
    if ObjectId.is_valid(board_id):
        board_id = ObjectId(board_id)
    else:
        return json_response({'message': 'Invalid board ID'}, 400)
    
    board = db.Boards.find_one({'_id': board_id, 'creatorID': g.user['_id']})
    
    if not board:
        return json_response({'message': 'Board not found or insufficient permissions'}, 404)
    email = data.get('email', '').strip()

    if not email:
        return json_response({'message': 'Missing email field'}, 400)

    if not is_valid_email(email):
        return json_response({'message': 'Invalid email format'}, 400)

    if email == g.user['email']:
        return json_response({'message': 'Cannot invite yourself'}, 400)

    user = db.Users.find_one({'email': email})

    if not user:
        return json_response({'message': 'User not found'}, 404)

    user_id = user['_id']

    if user_id in board['invited']:
        return json_response({'message': 'User already invited'}, 400)

    db.Boards.update_one({'_id': board_id}, {'$push': {'invited': user_id}, '$set': {'updatedAt': datetime.datetime.now()}})

    return json_response({'id': str(user_id), 'name': user['name'], 'email': user['email']})


@boards_bp.route('/<string:board_id>/invite', methods=['DELETE'])
@auth_required
def remove_user_from_board(board_id):
    data = request.json
    if not data:
        return json_response({'message': 'No data provided'}, 400)

    db = get_db()

    if ObjectId.is_valid(board_id):
        board_id = ObjectId(board_id)
    else:
        return json_response({'message': 'Invalid board ID'}, 400)

    board = db.Boards.find_one({'_id': board_id, 'creatorID': g.user['_id']})

    if not board:
        return json_response({'message': 'Board not found'}, 404)

    user_id = data.get('id')

    if not user_id:
        return json_response({'message': 'Missing user ID'}, 400)

    if ObjectId.is_valid(user_id):
        user_id = ObjectId(user_id)
    else:
        return json_response({'message': 'Invalid user ID'}, 400)

    if user_id not in board['invited']:
        return json_response({'message': 'User not invited'}, 400)

    db.Boards.update_one({'_id': board_id}, {'$pull': {'invited': user_id}, '$set': {'updatedAt': datetime.datetime.now()}})

    return json_response()