from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate

db = SQLAlchemy()


# def init_ext(app):
    
#     db.init_app(app)
#     migrate = Migrate(db=db)
#     migrate.init_app(app, db)
    
    # sess = Session()
    
    # sess.init_app(app)