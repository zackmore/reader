import pdb
import os.path
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref

Base = declarative_base()


class Admin(Base):
    __tablename__ = 'admin'

    userid = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)

    def __repr__(self):
        return '<Admin(username="%s")' % self.username


class Feed(Base):
    __tablename__ = 'feeds'

    feedid = Column(Integer, primary_key=True)
    feedname = Column(String, nullable=False)
    feedurl = Column(String, nullable=False)
    feedpubdate = Column(String)
    itemunread = Column(Integer)

    def __repr__(self):
        return '<Feed(feed="%s", url="%s")>' % (self.feedname,
                                                self.feedurl)


class Item(Base):
    __tablename__ = 'items'

    itemid = Column(Integer, primary_key=True)
    feedid = Column(Integer, ForeignKey('feeds.feedid'))
    feed = relationship('Feed', backref=backref('items',
                                                order_by=itemid))
    url = Column(String)
    pubdate = Column(String)
    title = Column(String, nullable=False)
    snippet = Column(String)
    content = Column(String)
    readed = Column(Boolean, default=False)
    star = Column(Boolean, default=False)
    guid = Column(String)

    def __repr__(self):
        return '<Item(title="%s", feed="%s")' % (self.title,
                                                self.feed.feedname)


db_file_path = 'sqlite:///' +\
                os.path.dirname(__file__) +\
                '/db/data.sqlite'
engine = create_engine(db_file_path)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
