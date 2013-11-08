# -*- coding: utf-8 -*-
import pdb

import os.path

import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options

from tornado.options import define, options
define('port', default=8000, help='run on the given port', type=int)

import db


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', IndexHandler),
            (r'/add_feed', AddFeedHandler),
            (r'/delete_feed', DeleteFeedHandler),
            (r'/feed/(\d+)', FeedHandler)
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            debug=True
        )
        tornado.web.Application.__init__(self, handlers, **settings)
        self.db = db.make_session()


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db


class IndexHandler(BaseHandler):
    def get(self):
        self.write('ok')


class FeedHandler(BaseHandler):
    pass


class AddFeedHandler(BaseHandler):
    pass


class DeleteFeedHandler(BaseHandler):
    pass


def echoOut():
    print('hello')


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = Application()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
