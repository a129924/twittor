import os

filepath = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{filepath}\\twittor.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "123456"
    TWEET_PER_PAGE = 2
    
    MAIL_DEFAULT_SENDER = 'noreply@twittor.com'
    MAIL_DEBUG = True
    MAIL_SERVER = 'smtp.office365.com'  # 郵件服務商的smtp
    MAIL_USERNAME = os.getenv('MAIL_USERNAME') or "YourEmail@outlook.com"  # email帳號
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD') or 'YourPassword'  # email密碼
    MAIL_PORT = 587  # stmp接口
    MAIL_USE_TLS = True  # 是否用TLS加密，outlook需要，其他邮箱不一定
    MAIL_DEFAULT_SENDER = ('FlaskRestful', MAIL_USERNAME)  # 可選擇(姓名，發送者電子郵件信箱)，也可以選擇單一電子信箱
