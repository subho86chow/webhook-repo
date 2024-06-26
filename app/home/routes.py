from flask import Blueprint, json, request, jsonify,render_template,current_app
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
    try:
        all_items = mongo.db.events.find().sort("timestamp", -1)
    except AttributeError:
        all_items = []
    return render_template('index.html', items=all_items)



# route for fetching data
@HomePage.route("/get-data-api", methods=['GET'])
def get_event_data():
    try:
        all_items = list(mongo.db.events.find({}).sort("timestamp", -1))
        for item in all_items:
            item['_id'] = str(item['_id'])
        return json.loads(json_util.dumps(all_items)) 
                   
    except AttributeError:
        return {'status':False},404


