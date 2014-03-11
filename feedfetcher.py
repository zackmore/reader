# -*- coding: utf-8 -*-

import os.path
import requests
import feedparser
import hashlib
import datetime
import time

from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from model import *
from helper import *

import pdb


class Fetcher(object):
    def __init__(self, feed_url):
        self.db = scoped_session(sessionmaker(bind=engine))
        self.result = feedparser.parse(feed_url)

    def parse_feed(self):
        try:
            self.feed = self.db.query(Feed).filter_by(
                            feedurl=self.result.feed.link).one()
        except:
            self.feed = Feed(
                            feedname=self.result.feed.title,
                            feedurl=self.result.feed.link,
                            feedpubdate = to_time(
                                self.result.feed.get('publishde_parsed',
                                    self.result.feed.get('updated_parsed')
                                )),
                            )

        for link in self.result.feed.links:
            if 'html' in link['type']:
                self.feed.sourceurl = link['href']

        if not self.feed.feedpubdate:
            self.feed.feedpubdate = to_time(time.gmtime())

    def _prepare_items(self, new_entries):
        if not len(new_entries):
            return False

        if not self.feed.itemunread:
            self.feed.itemunread = 0

        self.feed.itemunread += len(new_entries)

        for entry in new_entries:
            url = entry.link
            pubdate = to_time(entry.get('published_parsed',
                            entry.get('updated_parsed')
                                )
                            )
            title = entry.title
            snippet = entry.get('summary', entry.get('description'))
            content = entry.get('content', entry.get('description'))
            if isinstance(content, list):
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

    def parse_items(self):
        try:
            newest_item = self.db.query(Item).join(Feed).\
                        filter(Item.feedid==Feed.feedid).\
                        filter(Feed.feedname==self.feed.feedname).\
                        order_by(Item.pubdate.desc())[0]
        except:
            self._prepare_items(self.result.entries)
        else:
            sorted_entries = {}
            for entry in self.result.entries:
                entry_time = to_time(entry.get('published_parsed',
                                entry.get('updated_parsed')
                                    )
                                )
                sorted_entries[entry_time] = entry

            entry_times = sorted_entries.keys()
            entry_times.sort(reverse=True)

            new_entries = []
            for entry_time in entry_times:
                tmp_entry = sorted_entries[entry_time]
                tmp_guid = hashlib.md5(to_utf8(tmp_entry.title+tmp_entry.link)).hexdigest()

                if tmp_guid != newest_item.guid:
                    new_entries.append(tmp_entry)
                else:
                    break

            self._prepare_items(new_entries)

    def save_to_db(self):
        self.db.add(self.feed)
        self.db.commit()



if __name__ == '__main__':
    dumper = Fetcher('http://solidot.org.feedsportal.com/c/33236/f/556826/index.rss')
    #dumper = Fetcher('http://jandan.net/feed')
    #dumper = Fetcher('./testfeed.xml')
    #dumper = Fetcher('http://blog.zengq.in/feed.xml')
    #dumper = Fetcher('http://www.baibanbao.net/feed')
    dumper.parse_feed()
    dumper.parse_items()
    dumper.save_to_db()

