import sys
import os.path
import json
import datetime
import time

from tornado.ioloop import PeriodicCallback

import pdb

# Help functions
def to_unicode(value):
    if isinstance(value, unicode):
        return value
    if isinstance(value, basestring):
        return value.decode('utf-8')
    if isinstance(value, int):
        return str(value)
    if isinstance(value, bytes):
        return value.decode('utf-8')
    return value

def to_utf8(value):
    if isinstance(value, (bytes, type(None), str)):
        return value
    if isinstance(value, int):
        return str(value)
    assert isinstance(value, unicode)
    return value.encode('utf-8')

def to_time(timetuple):
    return time.strftime('%Y-%m-%d %H:%M:%S', timetuple)

def parse_time(value):
    if not value:
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, float):
        return datetime.fromtimestamp(value)
    try:
        return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
    except ValueError as e:
        print('Unrecorgnized time format. Error: %s' % e)
        sys.exit()


class QueryParser(object):
    def __init__(self, request_query):
        self.request_query = request_query
        self.arguments = {'mode': 'normal', 'more': 1}

        if '=' not in request_query:
            return

        pairs = request_query.split('&')
        for pair in pairs:
            key, value = pair.split('=')
            self.arguments[key] = value

    @property
    def mode(self):
        return str(self.arguments['mode'])

    @property
    def more(self):
        return int(self.arguments['more'])


class Pagination(object):
    def __init__(self, page_number, all_items_number, per_page):
        self.page_number = page_number
        self.per_page = per_page
        self.pages = all_items_number / per_page
        if all_items_number % per_page != 0:
            self.pages += 1

    @property
    def start_point(self):
        return (self.page_number - 1) * self.per_page
    
    @property
    def end_point(self):
        return (self.page_number - 1) * self.per_page + self.per_page

    @property
    def has_prev(self):
        return self.page_number > 1

    @property
    def prev_number(self):
        return self.page_number - 1

    @property
    def has_next(self):
        return self.page_number < self.pages

    @property
    def next_number(self):
        return self.page_number + 1


if __name__ == '__main__':
    a = QueryParser('mode=all&more=4')
