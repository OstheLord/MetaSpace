from flask import Flask, Blueprint, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

from your_room_controller_module import create_room, update_room, delete_room, get_room
from your_user_controller_module import create_user, update_user, delete_user, get_user, authenticate_user

bp = Blueprint('bp', __name__)
app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'your_secret_key'
jwt = JWTManager(app)

@bp.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400

    user_id = authenticate_user(username, password)
    if user_id is None:
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=user_id)
    return jsonify(access_token=access_token), 200

@bp.route('/rooms', methods=['POST'])
@jwt_required()
def create_room_route():
    response = create_room(request.get_json())
    return jsonify(response)

@bp.route('/rooms/<room_id>', methods=['GET'])
@jwt_required()
def get_room_route(room_id):
    response = get_room(room_name)
    return jsonify(response)

@bp.route('/rooms/<room_id>', methods=['PUT'])
@jwt_required()
def update_room_route(room_id):
    response = update_room(room_id, request.get_json())
    return jsonify(response)

@bp.route('/rooms/<room_id>', methods=['DELETE'])
@jwt_required()
def delete_room_route(room_id):
    response = delete_room(room_id)  # Fixed typo in parameter name
    return jsonify(response)

@bp.route('/users', methods=['POST'])
def create_user_route():
    response = create_user(request.get_json())
    return jsonify(response)

@bp.route('/users/<user_id>', methods=['GET'])
@jwt_required()
def get_user_route(user_id):
    response = get_user(user_id)
    return jsonify(response)

@bp.route('/users/<user_id>', methods=['PUT'])
@jwt_required()
def update_user_route(user_id):
    response = update_user(user_id, request.get_json())
    return jsonify(response)

@bp.route('/users/<user_id>', methods=['DELETE'])
@jwt_required()
def delete_user_route(user_id):
    response = delete_user(user_id)
    return jsonify(response)

app.register_blueprint(bp, url_prefix="/api")  # Corrected argument name

if __name__ == '__main__':
    app.run(debug=True)