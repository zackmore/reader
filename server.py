import os.path
import json
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options

from model import *
import helper

from tornado.options import define, options
define('port', default=9999, help='run on the given port', type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', MainHandler),
            (r'/feed/(\d+)', FeedHandler),
            (r'/item/(\d+)', ItemHandler),
            (r'/login', LoginHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__),
                                        'templates'),
            static_path=os.path.join(os.path.dirname(__file__),
                                        'templates/static'),
            ui_modules={'Sidebar': SidebarModule},
            cookie_secret='1234',
            #xsrf_cookies=True,
            debug=True
        )
        tornado.web.Application.__init__(self, handlers, **settings)
        self.db = scoped_session(sessionmaker(bind=engine))


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user_id = self.get_secure_cookie('uid')
        if user_id:
            try:
                user = self.db.query(Admin).filter_by(userid=user_id).one()
            except NoResultFound:
                return
            else:
                return user

    @property
    def db(self):
        return self.application.db


class SidebarModule(tornado.web.UIModule):
    def render(self):
        all_feeds = self.handler.db.query(Feed).order_by(Feed.feedid)
        return self.render_string('sidebar.html', all_feeds=all_feeds, admin_user=self.current_user)


class LoginHandler(BaseHandler):
    def post(self):
        if self.current_user:
            return

        username = self.get_argument('username')
        password = self.get_argument('password')

        result = self.db.query(Admin).\
                filter_by(username=username).\
                filter_by(password=password)

        if result.count():
            self.set_secure_cookie('uid', str(result.one().userid))
            self.redirect('/')
        else:
            return


class MainHandler(BaseHandler):
    def get(self):
        mode = self.get_argument('mode', 'normal')
        items_step = int(self.get_argument('more', 0))

        flag_offset = items_step * helper.CONFIG['Global']['more_quantity']

        if mode == 'all':
            newest_items = self.db.query(Item).\
                            order_by(Item.pubdate.desc()).\
                            offset(flag_offset).\
                            limit(helper.CONFIG['Global']['more_quantity'])
            items_quantity = self.db.query(Item).count()
        else:
            newest_items = self.db.query(Item).\
                            filter(Item.readed==0).\
                            order_by(Item.pubdate.desc()).\
                            offset(flag_offset).\
                            limit(helper.CONFIG['Global']['more_quantity'])
            items_quantity = self.db.query(Item).filter(Item.readed==0).count()

        next_step = int(items_step) + 1

        if items_quantity - flag_offset <= 10:
            flag_no_more = True
        else:
            flag_no_more = False

        self.render('list.html',
                    newest_items=newest_items,
                    next_step=next_step,
                    flag_no_more=flag_no_more)


class FeedHandler(BaseHandler):
    def get(self, feedid):
        items_step = int(self.get_argument('more', 0))
        flag_offset = items_step * helper.CONFIG['Global']['more_quantity']

        items = self.db.query(Item).filter_by(feedid=feedid).\
                order_by(Item.pubdate.desc()).\
                offset(items_step*helper.CONFIG['Global']['more_quantity']).\
                limit(helper.CONFIG['Global']['more_quantity'])

        items_quantity = self.db.query(Item).filter(Item.readed==0).count()

        next_step = int(items_step) + 1

        if items_quantity - flag_offset <= 10:
            flag_no_more = True
        else:
            flag_no_more = False

        self.render('list.html', newest_items=items,
                    next_step=next_step, flag_no_more=flag_no_more)


class ItemHandler(BaseHandler):
    def get(self, itemid):
        item = self.db.query(Item).filter_by(itemid=itemid).one()

        self.render('article.html', article=item)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)

    tornado.ioloop.IOLoop.instance().start()
