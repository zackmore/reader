import sys
import os.path
import json
import datetime
import time

import pdb


# Get config
config_file = file(os.path.join(os.path.dirname(__file__),
                                'config.json'), 'r')
CONFIG = json.loads(config_file.read())
config_file.close()


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

def HELP_snippet_trunc(text_string):
    return text_string[:30]
