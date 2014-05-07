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

host = config.get("Graph","host")
port = int(config.get("Graph","port"))
user = config.get("Graph","user")
passwd = config.get("Graph","password")
db = config.get("Graph","database")
tb = config.get("Graph","table")

class BaseHandler(tornado.web.RequestHandler):
        def get_current_user(self):
                return self.get_secure_cookie("user")

class IndexHandler(BaseHandler):
        @tornado.web.authenticated
        def get(self):
		instanceList = []
                name = tornado.escape.xhtml_escape(self.current_user)
		instances = MySQL.MysqlQuery().query_select('select distinct hostip from DB_GRAPH.tb_instancelist ')
		for i in instances:
			instanceList.append(i[0])
		
                self.render('graph/main.html',title='result_test',username=name,instanceList=instanceList)

        def post(self):
                #name = tornado.escape.xhtml_escape(self.current_user)
                #ruleList = []
                #review_status_info = 0
                #upload_path = os.path.join(os.path.dirname(__file__),'../tmp')
                #info = []
                #self.render('index.html',title='result_test',items=info,status=review_status,ruleList=ruleList,username=name)
		pass

class GraphHandler(BaseHandler):
        def get(self):
		pass
                #name = 'None'
                #self.render("login.html",username=name)
        def post(self):
		pass
                #username = self.get_argument('username')
                #password = self.get_argument('password')
                #password_p =  MySQL.MysqlQuery().query_select('select password("%s")' %(password))[0][0]
                #t = Auth()
                #password_e  = t.authPassword(username)
                #if ( password_e == password_p ):
                #        self.set_secure_cookie("user", self.get_argument("username"))
                #        self.redirect('/', permanent=True)
                ##else:
                 #       self.redirect('/login', permanent=True)

#if __name__ == "__main__":

