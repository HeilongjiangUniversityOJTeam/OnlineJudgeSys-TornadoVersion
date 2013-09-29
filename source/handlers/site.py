# -*- coding:utf-8 -*-

import tornado.web


class IndexHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user_info")

    def get(self):
        if self.current_user:
            name = self.current_user
        else:
            name = "None"
        self.render("index.html", curuser=name)


class StatusHandler(tornado.web.RequestHandler):
    def get(self):
        db = self.application.db.judge_queues
        self.render("status.html", status_list=db.find().sort('_id', -1).limit(10))


class ComplieErrInfoHandler(tornado.web.RequestHandler):
    def get(self, id):
        db = self.application.db.judge_queues.find_one({'_id': int(id)})

        if not db or not db['result']['err_code']:
            return self.write('404, id not exist')

        self.render('error_msg.html', msg=db['result']['err_code'])


class RankHandler(tornado.web.RequestHandler):
    def get(self):
        db = self.application.db.users
        self.render("rank.html", users=db.find({'group': 'student'}))
