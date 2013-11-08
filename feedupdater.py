import requests
import bs4
import datetime
import sys
import email.utils
import hashlib

from db import *
import pdb

class FeedUpdater(object):
    def rfc3339_to_time(self, time_str):
        try:
            time = time_str[0:19]
        except IndexError:
            print('Not long enough for an RFC3339 time format')
        time = datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%S')
        return time

    def rfc822_to_time(self, time_str):
        time = email.utils.parsedate_tz(time_str)
        if time:
            return time
        else:
            print('Not a valid RFC822 time format')

    def __init__(self, feed_url):
        self.feed_url = feed_url
        self.soup = ''
        self.db = make_session()
        #feed = self.db.query(Feed).filter(Feed.url==self.feed_url)[0]
        #self.last_update_time = feed.last_update_time
        self.last_update_time = self.rfc3339_to_time('2011-11-11T11:11:11')
        self.last_entry_code = '1111111111111111111111111111111111111111'

    def pre_process(self):
        try:
            r = requests.get(self.feed_url)
        except:
            print('Could not get the feed url')
            sys.exit(1)

        html = r.text
        self.soup = bs4.BeautifulSoup(html)
        if bool(self.soup.find('rss')): 
            self.rss_parse()
        if bool(self.soup.find('feed')): 
            self.atom_parse()

    def atom_parse(self):
        if self.soup.feed.updated:
            update_time = self.rfc3339_to_time(self.soup.feed.updated.text)
        else:
            update_time = datetime.datetime.now()

        if update_time > self.last_update_time:
            entries = self.soup.find_all('entry')
            for entry in entries:
                if hashlib.sha1(entry.text.encode('utf-8')).hexdigest() !=\
                self.last_entry_code:
                    # Add new record in database
                    pass
                else:
                    break
            # Update last_update_time, last_entry_code in Feed

    def rss_parse(self):
        if self.soup.rss.channel.pubDate:
            update_time = self.rfc822_to_time(self.soup.rss.channel.pubDate)
        elif self.soup.rss.channel.lastBuildDate:
            update_time = self.rfc822_to_time(
                            self.soup.rss.channel.lastBuildDate)
        else:
            update_time = datetime.datetime.now()

        if update_time > self.last_update_time:
            entries = self.soup.find_all('item')
            for entry in entries:
                if hashlib.sha1(entry.text.encode('utf-8')).hexdigest() !=\
                self.last_entry_code:
                    print 'add a new one'
                else:
                    break
            # Update last_update_time, last_entry_code in Feed


if __name__ == '__main__':
    #URL = 'http://yuehu.me/feed'
    URL = 'http://feeds2.feedburner.com/jandan'
    feedupdater = FeedUpdater(URL)
    feedupdater.pre_process()
