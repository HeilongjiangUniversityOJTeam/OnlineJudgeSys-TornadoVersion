#!/usr/bin/env python
# -*- coding:utf-8 -*-

import tornado.web
import tornado.httpserver
import tornado.options
import tornado.ioloop
import tornado.auth
import pymongo
import os.path
from tornado.options import define, options

from urls import urls

define("port", default=8888, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = urls

        settings = {
            "template_path": os.path.join(os.path.dirname(__file__), "templates"),
            "static_path": os.path.join(os.path.dirname(__file__), "static"),
            "cookie_secret": "123456789",
            "login_url": "/",
            "debug": True,
        }
        conn = pymongo.Connection("localhost", 27017)
        self.db = conn["Gaea"]
        tornado.web.Application.__init__(self, handlers, **settings)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()