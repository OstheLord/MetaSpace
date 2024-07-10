from flask import Flask, Blueprint, request, jsonify
from your_room_controller_module import create_room, update_room, delete_room, get_room
from your_user_controller_module import create_user, update_user, delete_user, get_user

bp = Blueprint('bp', __name__)

@bp.route('/rooms', methods=['POST'])
def create_room_route():
    data = request.get_json()
    response = create_room(data)
    return jsonify(response)

@bp.route('/rooms/<room_id>', methods=['GET'])
def get_room_route(room_id):
    response = get_context(room_id)
    return jsonify(response)

@bp.route('/rooms/<room_id>', methods=['PUT'])
def update_room_route(room_id):
    data = request.get_json()
    response = update_room(room_id, data)
    return jsonify(response)

@bp.route('/rooms/<room_id>', methods=['DELETE'])
def delete_room_route(room_id):
    response = delete_room(room_id)
    return jsonify(response)

@bp.route('/users', methods=['POST'])
def create_user_route():
    data = request.get_json()
    response = create_user(data)
    return jsonify(response)

@bp.route('/users/<user_id>', methods=['GET'])
def get_user_route(user_id):
    response = get_user(user_id)
    return jsonify(response)

@bp.route('/users/<user_id>', methods=['PUT'])
def update_user_route(user_id):
    data = request.get_json()
    response = update_user(user_id, data)
    return jsonify(response)

@bp.route('/users/<user_id>', methods=['DELETE'])
def delete_user_route(user_id):
    response = delete_user(userid)
    return jsonify(response)

app = Flask(__name__)
app.register_blueprint(bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)