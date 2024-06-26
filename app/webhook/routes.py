from flask import Blueprint, json, request, jsonify, current_app
from datetime import datetime 
from app.extensions import mongo
webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')


# receiver webhook end-point
@webhook.route('/receiver', methods=["POST"])
def receiver():
    data = request.json
    event_type = request.headers.get('X-Github-Event')

    if not event_type:
        return jsonify({"error": "Missing GitHub event type"}), 400

    event_data = None

    if event_type == 'push':
        event_data = {
            'author': data['pusher']['name'],
            'to_branch': data['ref'].split('/')[-1],
            'timestamp': datetime.utcnow(),
            'action_type': 'push'
        }
    elif event_type == 'pull':
        event_data = {
            'author': data['pull_request']['user']['login'],
            'from_branch': data['pull_request']['head']['ref'],
            'to_branch': data['pull_request']['base']['ref'],
            'timestamp': datetime.utcnow(),
            'action_type': 'pull_request'
        }
    elif event_type == 'merge':
        event_data = {
            'author': data['pull_request']['merged_by']['login'],
            'from_branch': data['pull_request']['head']['ref'],
            'to_branch': data['pull_request']['base']['ref'],
            'timestamp': datetime.utcnow(),
            'action_type': 'merge'
        }

    if event_data:
        print(event_data)
        try:
            result = mongo.db.events.insert_one(event_data)
            event_data['_id'] = str(result.inserted_id)
            print("Data saved to MongoDB:", event_data)
            return {jsonify(event_data)}, 200
        except Exception as e:
            print("Failed to save data to MongoDB:", e)
            return jsonify({"error": "Failed to save data to MongoDB"}), 500
    else:
        print("Unsupported event type:", event_type)
        return jsonify({"error": "Unsupported event type"}), 400