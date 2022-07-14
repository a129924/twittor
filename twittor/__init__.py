from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

from twittor.route import index, login  # NOQA: E402

def create_app():
    app = Flask(__name__)
    
    db.init_app(app)
    migrate.init_app(app, db)
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////:twittor.db" # 要////
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config['SQLALCHEMY_COMMIT_TEARDOWN'] = True
    
    app.config['SECRET_KEY'] = "123456"
    app.add_url_rule('/index',"index",index) # 等同於@app.route("/")
    app.add_url_rule('/login',"login",login,methods = ["GET", "POST"]) 
    
    return app

