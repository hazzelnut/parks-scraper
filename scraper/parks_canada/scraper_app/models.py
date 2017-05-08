from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

import settings


DeclarativeBase = declarative_base()


def db_connect():
    """
    Performs database connections using database settings from settings.py
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**settings.DATABASE))


def create_parks_table(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)


class Parks(DeclarativeBase):
    """Sqlalchemy parks model"""
    __tablename__ = "parks"

    id = Column(Integer, primary_key=True)
    name = Column('name', String)
    summary = Column('summary', String, nullable=True)
    about = Column('about', String, nullable=True)
    type = Column('type', String)
    lat = Column('lat', String)
    long = Column('long', String)
    province = Column('province', String)
    
