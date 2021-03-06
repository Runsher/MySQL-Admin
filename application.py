#!/usr/bin/python
#-*- encoding:utf-8 -*-
import sys
sys.path.append('/root/yeq/soft/SQL_Review0416/controllers')
import tornado.ioloop
import tornado.web
import shutil
import os
import Home
import Upload
import Review
import Rule
import Login
import Graph
import Crontab

from tornado.options import define, options
define("port", default = 5000, help = "run on the given port", type = int)

settings = {
       	"cookie_secret" : "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
       	"login_url"     : "/login",
        "static_path"   : os.path.join(os.path.dirname(__file__), "static"),
        "template_path" : os.path.join(os.path.dirname(__file__), "templates"),
        #"xsrf_cookies"  : True,
	"debug" : True,
        }


if __name__ == '__main__':
	tornado.options.parse_command_line()
	app=tornado.web.Application(
        	handlers=[
                	(r'/',Home.IndexHandler),
                	(r'/login',Login.LoginHandler),
                	(r'/review',Login.IndexHandler),
                	(r'/reviewco',Review.ReviewContent),
                	(r'/reviewfi',Review.ReviewFile),
                	(r'/rule',Rule.Rule),
                	(r'/crontab',Crontab.IndexHandler),
                	(r'/getlist',Crontab.GetList),
                	(r'/saveitem',Crontab.SaveItem),
                	(r'/updateitem',Crontab.UpdateItem),
                	(r'/destroyitem',Crontab.DestroyItem),
             #   	(r'/datamaintain',Crontab.DataMaintainHandler),
                	(r'/graph',Graph.IndexHandler),
                	#(r'/test',Review.Test),
                	],**settings
        	)

	http_server = tornado.httpserver.HTTPServer(app)
        http_server.listen(options.port)
        tornado.ioloop.IOLoop.instance().start()
