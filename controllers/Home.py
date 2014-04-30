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

ruleList = []
info = []
review_status = 0



class BaseHandler(tornado.web.RequestHandler):
        def get(self):
	#	return self.get_secure_cookie("user")
		pass

class IndexHandler(tornado.web.RequestHandler):
	#@tornado.web.authenticated
        def get(self):
#		name = tornado.escape.xhtml_escape(self.current_user)
                self.render('index.html',title='result_test',items=info,status=review_status,ruleList=ruleList)


	#@tornado.web.authenticated
        def post(self):
		ruleList = []
                review_status_info = 0
                upload_path = os.path.join(os.path.dirname(__file__),'../tmp')
                info = []
                self.render('index.html',title='result_test',items=info,status=review_status,ruleList=ruleList)
