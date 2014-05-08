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

config = ConfigParser.ConfigParser()
config.readfp(open("conf/adm.conf"),"rb")

host = config.get("Crontab","host")
port = int(config.get("Crontab","port"))
user = config.get("Crontab","user")
passwd = config.get("Crontab","password")
db = config.get("Crontab","database")
tb = config.get("Crontab","tb")

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

class GetList(BaseHandler):
        @tornado.web.authenticated
        def post(self):
		infos = []
		info = MySQL.MysqlQuery().query_select('select hostip,port,db_name,sql_command,last_act_date,interval_day,status,add_date from %s.%s' %(db,tb))
		maxrows = MySQL.MysqlQuery().query_select('select count(1) from %s.%s' %(db,tb))
		for i in info:
			infos.append({"host":i[0],"port":i[1],"db":i[2],"command":i[3],"interval":i[5],"level":i[6]})
		a = {
			"total" : maxrows,
			"rows"	: infos
		}
		self.write(a)

        def get(self):
                pass

class SaveItem(BaseHandler):
	@tornado.web.authenticated
        def post(self):
		pass

class UpdateItem(BaseHandler):
        @tornado.web.authenticated
        def post(self):
                pass

class DestroyItem(BaseHandler):
        @tornado.web.authenticated
        def post(self):
                pass
