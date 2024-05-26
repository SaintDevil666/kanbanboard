from flask import Blueprint, request, g, send_file
from bson import ObjectId
from io import BytesIO
from db import get_db
from utils import auth_required, json_response

uploads_bp = Blueprint('uploads', __name__)


@uploads_bp.route('/<string:card_id>', methods=['POST'])
@auth_required
def upload_file():
    if not ObjectId.is_valid(card_id):
        return json_response({'message': 'Invalid card ID'}, 400)
    if 'file' not in request.files:
        return json_response({'message': 'No file uploaded'}, 400)
    file = request.files['file']

    if file.filename == '':
        return json_response({'message': 'No file selected'}, 400)

    if not file or not file.content_type:
        return json_response({'message': 'Invalid file'}, 400)

    if file.content_length > 10 * 1024 * 1024:  # Перевірка розміру файлу (не більше 10МБ)
        return json_response({'message': 'File size exceeds the limit'}, 400)

    file_data = file.read()

    db = get_db()
    card = db.Cards.find_one({'_id': ObjectId(card_id)})
    if not card:
        return json_response({'message': 'Card not found'}, 404)

    result = db.Uploads.insert_one({
        'filename': file.filename,
        'mimetype': file.content_type,
        'data': file_data,
        'cardID': card['_id']
    })

    file_id = str(result.inserted_id)

    return json_response({'fileID': file_id, 'filename': file.filename}, 201)


@uploads_bp.route('/<string:file_id>', methods=['GET'])
@auth_required
def get_file(file_id):
    try:
        file_id = ObjectId(file_id)
    except:
        return json_response({'message': 'Invalid file ID'}, 400)
    
    db = get_db()

    file_data = db.Uploads.find_one({'_id': file_id})

    if not file_data:
        return json_response({'message': 'File not found'}, 404)

    file_content = BytesIO(file_data['data'])
    print(file_data)
    return send_file(file_content, mimetype=file_data['mimetype'], as_attachment=False, download_name=file_data['filename'])


@uploads_bp.route('/<string:file_id>', methods=['DELETE'])
@auth_required
def delete_file(file_id):
    if not ObjectId.is_valid(file_id):
        return json_response({'message': 'Invalid file ID'}, 400)
    
    db = get_db()
    result = db.Uploads.delete_one({'_id': ObjectId(file_id)})

    if result.deleted_count == 0:
        return json_response({'message': 'File not found'}, 404)

    return json_response()