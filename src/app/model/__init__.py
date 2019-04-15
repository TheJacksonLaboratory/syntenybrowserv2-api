from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
session_factory = sessionmaker(autoflush=False,
                               autocommit=False)
Session = scoped_session(session_factory)
Base.query = Session.query_property()


def init_db(app):
    """
    This method takes the current flask app and uses the 'SQLALCHEMY_DATABASE_URI' config property to create
    an sqlalchemy engine and attach it to the session factory.

    :param app: The flask app returned from app_factory
    :return: sqlalchemy engine, just in case you want it
    """
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    session_factory.configure(bind=engine)
    create_all(engine)
    return engine


def create_all(engine):
    # from .hello_world_model import Hello
    Base.metadata.create_all(engine, checkfirst=True)

def drop_all(engine):
    Base.metadata.drop_all(engine)

# from .hello_world_model import Hello
