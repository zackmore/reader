# -*- coding: utf-8 -*-

import os.path
import requests
import feedparser
import hashlib
import time

from sqlalchemy.orm import scoped_session, sessionmaker

from model import *

import pdb


class Fetcher(object):
    def __init__(self, feed_url):
        self.data = feedparser.parse(feed_url)
        self.session = scoped_session(sessionmaker(bind=engine))

        pdb.set_trace()

    def dump_feed(self):
        self.feed = Feed(
                        feedname=self.data.feed.title,
                        feedurl=self.data.feed.link,
                        feedpubdate=time.strftime('%Y-%m-%d %H:%M:%S',
                            self.data.feed.get('published_parsed',
                                self.data.feed.get('updated_parsed')
                            )
                        ),
                    )

    def dump_items(self):
        for entry in self.data.entries:
            url = entry.link
            pubdate = time.strftime('%Y-%m-%d %H:%M:%S',
                        entry.get('published_parsed',
                            entry.get('updated_parsed')
                        )
                    )
            title = entry.title
            snippet = entry.get('summary', entry.get('description'))
            content = entry.get('content', entry.get('description'))
            content = content[0].value
            guid = hashlib.md5((title+url).encode('utf-8')).hexdigest()

            item = Item(
                        url=url,
                        pubdate=pubdate,
                        title=title,
                        snippet=snippet,
                        content=content,
                        guid=guid
                    )
            self.feed.items.append(item)

    def check_pubdate(self):
        pdb.set_trace()

    def save_to_db(self):
        pdb.set_trace()
        self.session.add(self.feed)
        self.session.commit()



if __name__ == '__main__':
    dumper = Fetcher('./testfeed.xml')
    dumper.dump_feed()
    dumper.dump_items()
    #dumper.save_to_db()

