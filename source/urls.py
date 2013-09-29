# -*- coding:utf-8 -*-

from handlers.site import *
from handlers.help import *
from handlers.admin import *
from handlers.problem import *
from handlers.user import *

urls = []

urls.append((r"/", IndexHandler))
urls.append((r"/problems", ProblemsHandler))
urls.append((r"/problem/(\d+)", ShowProblemHandler))
urls.append((r"/status", StatusHandler))
urls.append((r"/status/(\d+)", ComplieErrInfoHandler))
urls.append((r"/ranklist", RankHandler))
urls.append((r"/submit/(\d+)", SubmitProblemHandler))

urls.append((r"/faq", FaqHandler))

urls.append((r"/user/(\w+)", UserInfoHandler))

urls.append((r"/register", RegisterUserHandler))
urls.append((r"/login", UserLoginHandler))
urls.append((r"/logout", UserLogoutHandler))

urls.append((r"/admin", AdminHomeHandler))
urls.append((r"/admin/login", AdminLoginHandler))
urls.append((r"/admin/logout", AdminLogoutHandler))
urls.append((r"/admin/add/problem", AddProblemHandler))
urls.append((r"/admin/add/data", AddDataFileIndexHandler))
urls.append((r"/admin/add/data/(\d+)", AddDataFileHandler))