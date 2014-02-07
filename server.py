import os.path
import json
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
            ui_modules={'Sidebar': SidebarModule},
            debug=True
        )
        tornado.web.Application.__init__(self, handlers, **settings)
        self.db = scoped_session(sessionmaker(bind=engine))


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db


class SidebarModule(tornado.web.UIModule):
    def render(self):
        all_feeds = self.handler.db.query(Feed).order_by(Feed.feedid)
        return self.render_string('sidebar.html', all_feeds=all_feeds)


class MainHandler(BaseHandler):
    def get(self):
        all_feeds = self.db.query(Feed).order_by(Feed.feedid)

        mode = self.get_argument('mode', 'normal')
        items_step = self.get_argument('more', 0)
        if mode == 'all':
            newest_items = self.db.query(Item).\
                            order_by(Item.pubdate.desc()).\
                            offset(items_step*
                                CONFIG['Global']['more_quantity']).\
                            limit(CONFIG['Global']['more_quantity'])
        else:
            newest_items = self.db.query(Item).\
                            filter(Item.readed==False).\
                            order_by(Item.pubdate.desc()).\
                            offset(items_step*
                                CONFIG['Global']['more_quantity']).\
                            limit(CONFIG['Global']['more_quantity'])
        next_step = int(items_step) + 1

        self.render('list.html',
                    all_feeds=all_feeds,
                    newest_items=newest_items,
                    next_step=next_step)


class FeedHandler(BaseHandler):
    def get(self, feedid):
        items_step = self.get_argument('more', 0)
        items = self.db.query(Item).filter_by(feedid=feedid).\
                order_by(Item.pubdate.desc()).\
                offset(items_step*CONFIG['Global']['more_quantity']).\
                limit(CONFIG['Global']['more_quantity'])
        next_step = int(items_step) + 1

        self.render('list.html', newest_items=items,
                    next_step=next_step)


class ItemHandler(BaseHandler):
    def get(self, itemid):
        item = self.db.query(Item).filter_by(itemid=itemid).one()

        self.render('article.html', article=item)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
