# -*- coding: utf-8 -*-

import os.path
import requests
import feedparser
import hashlib

from sqlalchemy.orm import scoped_session, sessionmaker

from model import *

import pdb


class Dumper(object):
    def __init__(self, feed_url):
        self.data = feedparser.parse(feed_url)
        self.session = scoped_session(sessionmaker(bind=engine))

    def dump_feed(self):
        self.feed = model.Feed(
                feedname=self.data.feed.title,
                feedurl=self.data.feed.link,
                #feedpubdate=self.data.feed.get('published_parsed',
                                                #'updated_parsed')
                )

    def dump_items(self):
        for entry in self.data.entries:
            url = entry.link
            #pubdate = entry.get('published_parsed', 'updated_parsed')
            pubdate = entry.get('published', 'updated')
            title = entry.title
            snippet = entry.get('summary', 'description')
            content = entry.get('content', 'description')
            guid = hashlib.md5(title+url).hexdigest()

            item = model.Item(
                        url=url,
                        pubdate=pubdate,
                        title=title,
                        snippet=snippet,
                        content=content,
                        guid=guid
                    )
            self.feed.items.append(item)

    def save_to_db(self):
        self.session.add(self.feed)
        self.session.commit()

    def check_pubdate(self):
        pass


if __name__ == '__main__':
    dumper = Dumper('./testfeed.xml')
    pdb.set_trace()
