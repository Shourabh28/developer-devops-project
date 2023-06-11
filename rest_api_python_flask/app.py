from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ
import json
from config import get_env_db_url

# Init app (create the instance of flask)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = get_env_db_url()
db = SQLAlchemy(app)

app.app_context().push()

class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.String(10), nullable=False)
    message_id = db.Column(db.String(20), nullable=False)
    sender_number = db.Column(db.String(20), nullable=False)
    receiver_number = db.Column(db.String(20), nullable=False)

    def __init__(self, account_id, message_id, sender_number, receiver_number):
        self.account_id = account_id
        self.message_id = message_id
        self.sender_number = sender_number
        self.receiver_number = receiver_number

    def json(self):
        return {'id': self.id, 'account_id': self.account_id, 'message_id': self.message_id, 'sender_number': self.sender_number, 'receiver_number': self.receiver_number}

db.create_all()

# Create a healthcheck route
@app.route('/healthz', methods=['GET'])
def test():
    return make_response(jsonify({'message': 'OK'}), 200)

# get all messages
@app.route('/all', methods=['GET'])
def get_all():
  try:
    all = Message.query.all()
    return make_response(jsonify([msg.json() for msg in all]), 200)
  except e:
    return make_response(jsonify({'message': 'error getting messages'}), 500)

# Get all the messages for an account_id
@app.route('/get/messages/<account_id>', methods=['GET'])
def get_messages(account_id):
    try:
        msg = Message.query.filter_by(account_id=account_id)
        if msg:
            return make_response(jsonify([acc.json() for acc in msg]), 200)
        return make_response(jsonify({'message': 'account_id not found !!!'}), 404)
    except e:
        return make_response(jsonify({'message': 'error getting account_id'}), 500)

# Save new message with details
@app.route('/create', methods=['POST'])
def save_message_details():
    try:
        data = json.loads(request.data, strict=False)
        new_message = Message(account_id=data['account_id'], message_id=data['message_id'], sender_number=data['sender_number'], receiver_number=data['receiver_number'])
        db.session.add(new_message)
        db.session.commit()
        return make_response(jsonify({'message': 'message saved'}), 201)
    except e:
        return make_response(jsonify({'message': 'error saving the message details'}), 500)

# search for keys
@app.route('/search', methods=['GET'])
def search_message():
    try:
        query_params = request.args.to_dict()
        output = []
        # search_param = {"message_id", "sender_number", "receiver_number"}
        # searched_param = set(query_params.keys()).intersection(search_param)

        ## 
        # def search_message_with_param(x="message_id" or "sender_number" or "receiver_number"):
        #     list_x = query_params[x].replace('"','').split(',')
        #     for x_id in list_x:
        #         y_id = Message.query.filter_by(x=x_id)
        #         if y_id and [msgs.json() for msgs in y_id]:
        #             return [msgs.json() for msgs in y_id]
        
        if "message_id" in query_params:
            list_message_id = query_params["message_id"].replace('"','').split(',')
            for m_id in list_message_id:
                msg_id = Message.query.filter_by(message_id=m_id)
                if msg_id and [msgs.json() for msgs in msg_id]:
                    output.append([msgs.json() for msgs in msg_id])
                
        if "sender_number" in query_params:
            list_sender_number = query_params["sender_number"].replace('"','').split(',')
            for s_no in list_sender_number:
                sender_no = Message.query.filter_by(sender_number=s_no)
                if sender_no and [sender.json() for sender in sender_no]:
                    output.append([sender.json() for sender in sender_no])
                
        if "receiver_number" in query_params:
            list_receiver_number = query_params["receiver_number"].replace('"','').split(',')
            for r_no in list_receiver_number:
                receiver_no = Message.query.filter_by(receiver_number=r_no)
                if receiver_no and [receiver.json() for receiver in receiver_no]:
                    output.append([receiver.json() for receiver in receiver_no])

        return make_response(jsonify(output), 200)
    except e:
        return make_response(jsonify({'message': 'error searching the message'}), 500)

# Run Server
if __name__ == '__main__':
    app.run(debug=True)
