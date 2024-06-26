from flask import Blueprint, json, request, jsonify,render_template
from app.extensions import *
from datetime import datetime
from bson import json_util
from app.extensions import mongo


HomePage = Blueprint('Home', __name__, url_prefix='/')


# date formatter template filter
def format_datetime(value, format="%d %B %Y - %I:%M %p UTC"):
    if value is None:
        return ""
    return datetime.strptime(str(value), '%Y-%m-%d %H:%M:%S.%f').strftime(format)

# route for home page
@HomePage.route('/', methods=["GET","POST"])
def home_page():
    all_items = mongo.db.events.find().sort("timestamp", -1)
    return render_template('index.html',items = all_items)



# route for fetching data
@HomePage.route("/get-data-api", methods=['GET'])
def get_event_data():
    all_items = list(mongo.db.events.find().sort("timestamp", -1))
    for item in all_items:
        item['_id'] = str(item['_id'])
    return json.loads(json_util.dumps(all_items)) 



