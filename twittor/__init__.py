from flask import Flask

from flask_migrate import Migrate


from twittor.ext import db
from twittor.route import index, login, logout, register, user_view, edit_profile, page_not_found, reset_password_request
from twittor.config import Config
from twittor.flask_login_manager import login_manager


app = Flask(__name__)
migrate = Migrate()
login_manager.login_view = "login"

def create_app():
    
    app.config.from_object(Config)
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    login_manager.init_app(app)

    app.add_url_rule('/index', "index", index, methods=["GET", "POST"])  # 等同於@app.route("/")
    app.add_url_rule("/", "index", index, methods=["GET", "POST"])
    app.add_url_rule('/login',"login", login,methods = ["GET", "POST"]) 
    app.add_url_rule("/logout", "logout",  logout)
    app.add_url_rule("/register", "register", register, methods=["GET", "POST"])
    app.add_url_rule("/<username>", "profile", user_view, methods=["GET", "POST"])
    app.add_url_rule("/edit_profile", "edit_profile", edit_profile, methods=["GET", "POST"])
    app.add_url_rule("/reset_password_request","reset_password_request", reset_password_request, methods=["GET", "POST"])
    app.register_error_handler(404, page_not_found)
    
    return app