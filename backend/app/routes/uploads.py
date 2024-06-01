from flask import Blueprint, request, g, send_file
from bson import ObjectId
import base64
from io import BytesIO
from db import get_db
from utils import auth_required, json_response

uploads_bp = Blueprint('uploads', __name__)


@uploads_bp.route('/<string:card_id>', methods=['POST'])
@auth_required
def upload_file(card_id):
    if not ObjectId.is_valid(card_id):
        return json_response({'message': 'Invalid card ID'}, 400)

    data = request.json
    if not data or 'file' not in data:
        return json_response({'message': 'No file uploaded'}, 400)

    file_data = data['file']

    filename = file_data.get('filename', '')
    mimetype = file_data.get('mimetype', '')
    file_base64 = file_data.get('data', '')

    if not filename or not file_base64 or not isinstance(mimetype, str):
        return json_response({'message': 'Invalid file data'}, 400)

    file_size = len(file_base64) * 3 / 4  # Розмір файлу в байтах

    if file_size > 10 * 1024 * 1024:  # Перевірка розміру файлу (не більше 10МБ)
        return json_response({'message': 'File size exceeds the limit'}, 400)

    db = get_db()
    card = db.Cards.find_one({'_id': ObjectId(card_id)})
    if not card:
        return json_response({'message': 'Card not found'}, 404)

    result = db.Uploads.insert_one({
        'filename': filename,
        'mimetype': mimetype,
        'data': file_base64,
        'cardID': card['_id']
    })

    file_id = str(result.inserted_id)

    return json_response({'fileID': file_id, 'filename': filename}, 201)

@uploads_bp.route('/<string:file_id>', methods=['GET'])
@auth_required
def get_file(file_id):
    if not ObjectId.is_valid(file_id):
        return json_response({'message': 'Invalid file ID'}, 400)
    
    db = get_db()

    file_data = db.Uploads.find_one({'_id': ObjectId(file_id)})

    if not file_data:
        return json_response({'message': 'File not found'}, 404)

    file_content = base64.b64decode(file_data['data'])
    file_content = BytesIO(file_content)

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