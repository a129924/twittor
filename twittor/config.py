import os

filepath = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{filepath}\\twittor.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "123456"
    TWEET_PER_PAGE = 2
