#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
import pdb

import sys
import os.path
import subprocess

from sqlalchemy.orm import scoped_session, sessionmaker

from model import *

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

        admin = Admin(username='admin', password='admin')
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
    elif command == 'server':
        subprocess.call(['python', 'server.py'])


if __name__ == '__main__':
    main()
