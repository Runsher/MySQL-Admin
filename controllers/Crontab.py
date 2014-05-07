#coding:utf-8
import tornado.httpserver
import tornado.web
import tornado.options
import tornado.ioloop
import sys
import MySQL
import ConfigParser

reload(sys)
sys.setdefaultencoding("utf8")

class BaseHandler(tornado.web.RequestHandler):
        def get_current_user(self):
                return self.get_secure_cookie("user")

class IndexHandler(BaseHandler):
        @tornado.web.authenticated
        def get(self):
                instanceList = []
                name = tornado.escape.xhtml_escape(self.current_user)
                self.render('crontab/main.html',title='crontab',username=name)

        def post(self):
		pass

class DataMaintainHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		name = tornado.escape.xhtml_escape(self.current_user)
		self.render('crontab/dataMaintain.html',title='crontab',username=name)

	def post(self):
                pass
