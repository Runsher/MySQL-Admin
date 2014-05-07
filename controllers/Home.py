#coding:utf-8
import os.path
import tornado.httpserver
import tornado.web
import tornado.options
import tornado.ioloop
import re
import sys
import ReviewPart
import MySQL
import Login

reload(sys)
sys.setdefaultencoding("utf8")




class BaseHandler(tornado.web.RequestHandler):
        def get_current_user(self):
		return self.get_secure_cookie("user")

class IndexHandler(BaseHandler):
	@tornado.web.authenticated
        def get(self):
		name = tornado.escape.xhtml_escape(self.current_user)
                self.render('index.html',username=name)


        def post(self):
		pass
