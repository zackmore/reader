# -*- coding: utf-8 -*-

import pdb
import os.path

from helper import *

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

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
    sourceurl = Column(String, nullable=False)
    feedurl = Column(String, nullable=False)
    feedpubdate = Column(String, nullable=True)
    #itemall = Column(Integer)
    itemunread = Column(Integer, default=0)

    def __repr__(self):
        return '<Feed(feed="%s", url="%s")>' % (self.feedname, self.feedurl)


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
        return '<Item(title="%s", feed="%s")' % (to_utf8(self.title), to_utf8(self.feed.feedname))


db_file_path = 'sqlite:///' + './db/data.sqlite'
engine = create_engine(db_file_path)

Base.metadata.create_all(engine)


if __name__ == '__main__':
    from sqlalchemy.orm import scoped_session, sessionmaker
    session = scoped_session(sessionmaker(bind=engine))

    #pdb.set_trace()

    #feed1 = Feed(feedname=u'虎嗅网', feedurl=u'http://huxiu.com/feed')
    #feed2 = Feed(feedname=u'白板报', feedurl=u'http://www.baibanbao.net/feed')

    #feed1_item1 = Item(feedid=1,
    #                    url=u'http://huxiu.com/article/27421/1.html',
    #                    pubdate=u'2014-02-08 06:31',
    #                    title=u'解剖Elon Musk的“黑洞型”营销',
    #                    snippet=u'好多年前，当科幻片还没今天这么多的时候……',
    #                    content=u'具体内容')
    #feed1_item2 = Item(feedid=1,
    #                    url=u'http://huxiu.com/article/27421/2.html',
    #                    pubdate=u'2014-02-08 05:31',
    #                    title=u'解剖Elon Musk的“黑洞型”营销2',
    #                    snippet=u'好多年前，当科幻片还没今天这么多的时候……',
    #                    content=u'具体内容2')
    #feed1.items.append(feed1_item1)
    #feed1.items.append(feed1_item2)

    #session.add_all([feed1, feed2])
    #session.commit()

    #pdb.set_trace()
