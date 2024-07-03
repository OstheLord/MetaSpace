from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

database = SQLAlchemy(app)

@app.before_request
def convert_json_request():
    if request.is_json:
        request.json_data = request.get_json()

class Room(database.Model):
    room_id = database.Column(database.Integer, primary_key=True)
    room_name = database.Column(database.String(120), nullable=False)

class User(database.Model):
    user_id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(80), unique=True, nullable=False)

@app.route('/rooms', methods=['POST', 'GET'])
def room_operations():
    if request.method == 'POST':
        if request.json_data:
            new_room = Room(room_name=request.json_data['name'])
            database.session.add(new_room)
            database.session.commit()
            return jsonify({"message": "Room created successfully"}), 201
        return jsonify({"error": "Bad request"}), 400
    else:
        all_rooms = Room.query.all()
        return jsonify([{'id': room.room_id, 'name': room.room_name} for room in all_rooms]), 200

@app.route('/users', methods=['POST', 'GET'])
def user_operations():
    if request.method == 'POST':
        if request.json_data:
            new_user = User(username=request.json_data['username'])
            database.session.add(new_user)
            database.session.commit()
            return jsonify({"message": "User created successfully"}), 201
        return jsonify({"error": "Bad request"}), 400
    else:
        all_users = User.query.all()
        return jsonify([{'id': user.user_id, 'username': user.username} for user in all_users]), 200

@app.before_first_request
def setup_database():
    database.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)