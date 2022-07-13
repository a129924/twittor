from flask import Flask
from twittor.route import index

def create_app():
    app = Flask(__name__)
    app.add_url_rule('/',"index",index) # 等同於@app.route("/")
    
    return app

