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
		info = MySQL.MysqlQuery().query_select('select id, hostip,port,db_name,sql_command,last_act_date,interval_day,status,add_date from %s.%s' %(db,tb))
		maxrows = MySQL.MysqlQuery().query_select('select count(1) from %s.%s' %(db,tb))
		for i in info:
			infos.append({"id":i[0],"host":i[1],"port":i[2],"db":i[3],"command":i[4],"interval":i[6],"level":i[7]})
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
		id = self.get_argument("id")
		db_host = self.get_argument("host")
		db_port = self.get_argument("port")
		db_name = self.get_argument("db")
		command = self.get_argument("command")
		interval = self.get_argument("interval")
		level = self.get_argument("level")
		MySQL.MysqlQuery().query_update('insert into %s.%s(hostip,port,db_name,sql_command,interval_day,status) values(%s,%s,%s,%s,%s,%s)' %(db,tb,db_host,db_port,db_name,command,interval,level))
		self.write(id)

class UpdateItem(BaseHandler):
        @tornado.web.authenticated
        def post(self):
                id = self.get_argument("id")
		db_host = self.get_argument("host")
		db_port = self.get_argument("port")
		db_name = self.get_argument("db")
		command = self.get_argument("command")
		interval = self.get_argument("interval")
		level = self.get_argument("level")
		#MySQL.MysqlQuery().query_update('update %s.%s set db_host="%s",db_port=%s,db_name="%s",command="%s",interval=%s,level=%s where id=%s' %(db,tb,db_host,db_port,db_name,command,interval,level,id))
		MySQL.MysqlQuery().query_update('update %s.%s set db_host="%s" where id=%s' %(db,tb,db_host,id))
		self.write(id)

class DestroyItem(BaseHandler):
        @tornado.web.authenticated
        def post(self):
		id = self.get_argument("id")
		MySQL.MysqlQuery().query_update('delete from  %s.%s where id=%s' %(db,tb,id))
		self.write(id)
