from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages')
def get_messages():  
    messages = Message.query.order_by(Message.created_at.asc()).all()
    message_list = []

    for message in messages:
        message_list.append({
            "id": message.id,  
            "body": message.body,  
            "created_at": message.created_at,
            "updated_at": message.updated_at
        })
    
    return jsonify(message_list)

@app.route('/messages', methods=["POST"])
def add_messages():
    data = request.get_json()
    body = data.get('body')
    username = data.get('username')

    if not body or not username:
        return jsonify({"error": "Both 'body' and 'username' are required"}), 400

    new_message = Message(body=body, username=username)
    db.session.add(new_message)
    db.session.commit()

    return jsonify({
        "id": new_message.id,
        "body": new_message.body,
        "username": new_message.username,
        "created_at": new_message.created_at,
        "updated_at": new_message.updated_at
    }), 201


@app.route('/messages/<int:message_id>', methods=["PATCH"])
def update_message(message_id):
    message = Message.query.get(message_id)

    if message:
        data = request.get_json()
        body = data.get('body', message.body) 
        username = data.get('username', message.username)

        message.body = body
        message.username = username
        db.session.commit()

        return jsonify({
            "id": message.id,
            "body": message.body,
            "username": message.username,
            "created_at": message.created_at,
            "updated_at": message.updated_at
        }), 200
    else:
        return jsonify({"error": "Message not found!"}), 404

    
@app.route('/messages/<int:message_id>', methods=["DELETE"])
def delete_message(message_id):
    message = Message.query.get(message_id)
    if message:
        db.session.delete(message)
        db.session.commit()
        return jsonify({"success": "Message deleted successfully"}), 200
    else:
        return jsonify({"error": "Message not found!"}), 404



if __name__ == '__main__':
    app.run(port=5555)
