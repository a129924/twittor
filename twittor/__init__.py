from flask import Flask
from twittor.route import index, login

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "123456"
    app.add_url_rule('/index',"index",index) # 等同於@app.route("/")
    app.add_url_rule('/login',"login",login,methods = ["GET", "POST"]) 
    
    return app

