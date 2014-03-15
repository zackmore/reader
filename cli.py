#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
import pdb

import sys
import os.path
import subprocess

from sqlalchemy.orm import scoped_session, sessionmaker

from config import *
from model import *
from feedfetcher import *

documentation = {}

documentation['help'] = '''Reader A Self-host RSS Reader
Usage:
    python cli.py init
    python cli.py fetch
    python cli.py server
    python cli.py help
'''

documentation['init'] = '''
'''

documentation['fetch'] = '''
'''

documentation['update'] = '''
'''

documentation['server'] = '''
'''


def main():
    db_file_path = 'sqlite:///' + './db/data.sqlite'
    engine = create_engine(db_file_path)
    session = scoped_session(sessionmaker(bind=engine))

    command = 'help'

    if len(sys.argv) >= 2:
        command = sys.argv[1]

    if command == 'help':
        print documentation['help']
    elif command == 'init':
        Base.metadata.create_all(engine)

        admin = Admin(username=Admin_username,
                    password=encrypt_password(Admin_username, Admin_password))
        session.add(admin)
        session.commit()
    elif command == 'fetch':
        try:
            feed_url = sys.argv[3]
        except IndexError:
            print 'fetch what?'
        else:
            dumper = Fetcher(feed_url)
            dumper.parse_feed()
            dumper.parse_items()
            dumper.save_to_db()
    elif command == 'update':
        feeds = session.query(Feed)
        if feeds.count():
            feeds = feeds.all()
            for feed in feeds:
                tmp_dumper = Fetcher(feed.feedurl)
                tmp_dumper.parse_feed()
                tmp_dumper.parse_items()
                tmp_dumper.save_to_db()
        else:
            print 'No feeds now, please fetch some.'
            return
    elif command == 'server':
        subprocess.call(['python', 'server.py'])


if __name__ == '__main__':
    main()
