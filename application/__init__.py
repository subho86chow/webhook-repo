from flask import Flask
from application.extensions import mongo
from application.webhook.routes import webhook
from flask_pymongo import PyMongo
from application.home.routes import HomePage,format_datetime


# Creating our flask app
def create_app():

    app = Flask(__name__)

    app.config["MONGO_URI"] = "mongodb://localhost:27017/webhooks_db"
    # app.config["MONGO_URI"] = "mongodb+srv://subho86chow:webhook_db@cluster0.cwcw5oc.mongodb.net/webhooks_db"
    mongo.init_app(app)

    # registering all template filter
    app.jinja_env.filters['datetime'] = format_datetime

    # registering all the blueprints
    app.register_blueprint(webhook)
    app.register_blueprint(HomePage)
    
    return app
