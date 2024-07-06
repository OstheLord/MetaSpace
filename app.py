from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URI', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.before_request
def ensure_json_request():
    if request.is_json:
        request.json_data = request.get_json()

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

@app.route('/rooms', methods=['POST', 'GET'])
def handle_rooms():
    if request.method == 'POST':
        room_data = request.json_data
        if room_data:
            new_room = Room(name=room_data['name'])
            db.session.add(new_room)
            db.session.commit()
            return jsonify({"message": "Room created successfully"}), 201
        return jsonify({"error": "Bad request - missing room name"}), 400
    else:
        rooms = Room.query.all()
        return jsonify([{'id': room.id, 'name': room.name} for room in rooms]), 200

@app.route('/users', methods=['POST', 'GET'])
def handle_users():
    if request.method == 'POST':
        user_data = request.json_data
        if user_data:
            new_user = User(username=user_data['username'])
            db.session.add(new_user)
            db.session.commit()
            return jsonify({"message": "User created successfully"}), 201
        return jsonify({"error": "Bad request - missing username"}), 400
    else:
        users = User.query.all()
        return jsonify([{'id': user.id, 'username': user.username} for user in users]), 200

@app.before_first_request
def initialize_database():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)