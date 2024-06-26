from flask import Flask
from app.extensions import mongo
from app.webhook.routes import webhook
from app.home.routes import HomePage,format_datetime


# Creating our flask app
def create_app():

    app = Flask(__name__)

    # db connection
    app.config["MONGO_URI"] = "mongodb://localhost:27017/webhooks_db"
    mongo.init_app(app)

    # registering all template filter
    app.jinja_env.filters['datetime'] = format_datetime

    # registering all the blueprints
    app.register_blueprint(webhook)
    app.register_blueprint(HomePage)
    
    return app
