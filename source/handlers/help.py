# -*- coding:utf-8 -*-

import tornado.web

class FaqHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("faq.html")
