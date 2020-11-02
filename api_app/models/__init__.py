'''
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
from flask_marshmallow import Marshmallow

DBSession = scoped_session(sessionmaker())
Base = declarative_base()
ma = Marshmallow()

def initialize_sql(app):
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    ma.init_app(app)
'''