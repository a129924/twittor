from flask import Flask

from flask_migrate import Migrate

from twittor.ext import db
from twittor.constants import DB_URL
from twittor.route import index, login
from twittor.config import Config

def create_app():
    app = Flask(__name__)
    migrate = Migrate()
    
    app.config.from_object(Config)
    
    db.init_app(app)
    migrate.init_app(app, db)

    app.config['SECRET_KEY'] = "123456"
    app.add_url_rule('/index',"index",index) # 等同於@app.route("/")
    app.add_url_rule('/login',"login",login,methods = ["GET", "POST"]) 
    
    return app

