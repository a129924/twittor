from .ext import db
import datetime

class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    create_date = db.Column(db.DateTime,default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    
    def __repr__(self):
        return f"id={self.id},body={self.body}, create_date={self.create_date}, user_id={self.user_id}"