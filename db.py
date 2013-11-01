# -*- coding: utf-8 -*-

import os.path

from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///db/app.db')
Base = declarative_base()

class Feed(Base):
    __tablename__ = 'feed'

    id = Column(Integer, primary_key=True)
    name = Column(String, default='Unknown')
    url = Column(String, nullable=False)
    last_update_time = Column(String)
    items = relationship('Item', backref='feed')

    def __init__(self, name, url, last_update_time):
        self.name = name
        self.url = url
        self.last_update_time = last_update_time

    def __repr__(self):
        return '<Feed %s[%s]>' % (self.name, self.url)


class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    pub_date = Column(String)
    readed = Column(Boolean, default=False)
    feed_id = Column(Integer, ForeignKey('feed.id'))

    def __init__(self, title, content, pub_date, readed):
        self.title = title
        self.content = content
        self. pub_date = pub_date
        self.readed = readed

    def __repr__(self):
        return '<Item %s>' % self.title


class StarredItem(Base):
    __tablename__ = 'starred_item'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    pub_date = Column(String)

    def __init__(self, title, content, pub_date):
        self.title = title
        self.content = content
        self. pub_date = pub_date

    def __repr__(self):
        return '<Starred Item %s>' % self.title


Base.metadata.create_all(engine)
