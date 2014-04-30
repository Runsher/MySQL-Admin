#coding:utf-8
import tornado.httpserver
import tornado.web
import tornado.options
import tornado.ioloop
import MySQL
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



class Auth():
        def __init__(self):
                pass;

        def authPassword(self,username):
                try:
                        password = MySQL.MysqlQuery().query_select('select password from DB_REVIEW_CONTROL.user where username="%s"' %(username))[0][0]
                        if password:
                                return password
                        else:
                                print "no user"
                except Exception,e:
                        print e

class BaseHandler(tornado.web.RequestHandler):
        def get_current_user(self):
                return self.get_secure_cookie("user")

class IndexHandler(BaseHandler):
        @tornado.web.authenticated
        def get(self):
                name = tornado.escape.xhtml_escape(self.current_user)
		self.render('index.html',title='result_test',items=info,status=review_status,ruleList=ruleList,username=name)
               
	def post(self):
                name = tornado.escape.xhtml_escape(self.current_user)
                ruleList = []
                review_status_info = 0
                upload_path = os.path.join(os.path.dirname(__file__),'../tmp')
                info = []
                self.render('index.html',title='result_test',items=info,status=review_status,ruleList=ruleList,username=name)

class LoginHandler(BaseHandler):
        def get(self):
		name = 'None'
		self.render("login.html",username=name)
        def post(self):
                username = self.get_argument('username')
                password = self.get_argument('password')
		password_p =  MySQL.MysqlQuery().query_select('select password("%s")' %(password))[0][0]
                t = Auth()
                password_e  = t.authPassword(username)
               	if ( password_e == password_p ):
                    	self.set_secure_cookie("user", self.get_argument("username"))
                       	self.redirect('/', permanent=True)
              	else:
                  	self.redirect('/login', permanent=True)

if __name__ == "__main__":
	t = Auth()
	username = 'admin'
	password = 'admin'
	password_p =  MySQL.MysqlQuery().query_select('select password("%s")' %(password))[0][0]
	password_e  = t.authPassword(username)
	print password_e,password_p 
	try:
             	if ( password_e == password_p ):
			print "user"
		else:
			print "w"
                      #	self.redirect('/', permanent=True)
             # 	else:
              #      	self.redirect('/login', permanent=True)
  	except Exception,e:
            	print e
