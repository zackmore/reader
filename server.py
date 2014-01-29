import os.path
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options

from sqlalchemy.orm import scoped_session, sessionmaker
from model import *
from helper import *

from tornado.options import define, options
define('port', default=9999, help='run on the given port', type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', MainHandler),
            (r'/feed/(\d+)', FeedHandler),
            (r'/item/(\d+)', ItemHandler)
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__),
                                        'templates'),
            static_path=os.path.join(os.path.dirname(__file__),
                                        'templates/static'),
            debug=True
        )
        tornado.web.Application.__init__(self, handlers, **settings)
        self.db = scoped_session(sessionmaker(bind=engine))


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db


class MainHandler(BaseHandler):
    def get(self):
        all_feeds = self.db.query(Feed).order_by(Feed.feedid)

        mode = self.get_argument('mode', 'normal')
        if mode == 'all':
            newest_items = self.db.query(Item).\
                            order_by(Item.pubdate.desc()).\
                            limit(CONFIG['Global']['more_quantity'])
        else:
            newest_items = self.db.query(Item).\
                            filter(Item.readed==False).\
                            order_by(Item.pubdate.desc()).\
                            limit(CONFIG['Global']['more_quantity'])

        self.render('list.html',
                    all_feeds=all_feeds,
                    newest_items=newest_items)


class FeedHandler(BaseHandler):
    def get(self, feedid):
        pass


class ItemHandler(BaseHandler):
    pass


if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
