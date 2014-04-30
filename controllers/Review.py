#coding:utf-8
import sys
import os.path
import tornado.web
import tornado.ioloop
import os
import re
import ConfigParser
import MySQL
import ReviewPart
import time
import datetime
import shutil

reload(sys)
sys.setdefaultencoding("utf8")

#now = time.localtime()
#str_now = time.strftime("%Y%m%d%H%M%S", now )

info = []
review_status = 0


class LoadAndClean():
	def find_Load(self,tmpfile):
            	MySQL.MysqlLoad().loadin(tmpfile)

	def moveFile(self,tmpfile):
		oldPath = tmpfile
		newPath =  os.path.join(os.path.dirname(__file__),'../sqlfile')
		shutil.move(oldPath,newPath)	

	def dropTmpDB(self,db):
		MySQL.MysqlQuery().query_update('drop database %s' %(db))



class ReviewContent(tornado.web.RequestHandler):
	def get(self):
		self.render('review.html',title='result_test',items=info,status=review_status)


	def post(self):
		now = time.localtime()
		str_now = time.strftime("%Y%m%d%H%M%S", now )
		review_status = 0
                upload_path = os.path.join(os.path.dirname(__file__),'../tmp')  
		info = []
		dbTmpName = 'DB_TMP'+str_now
		file_me = self.get_argument('content')
		if self.get_argument('content'):
			file_me = self.get_argument('content')
			filepath = upload_path+'/'+'tmpfile'+str_now
			f = open(filepath,'w')
			f.write(file_me)
			f.close()
                       	LoadAndClean().find_Load(filepath)
			db = MySQL.tmpDB
                       	max_id = MySQL.MysqlQuery().query_select('select max(id) from DB_REVIEW_CONTROL.tb_review_result')[0][0]
                       	tb_name = MySQL.MysqlQuery().query_select('show tables from %s' %(db))
                     	if tb_name:
                              	for tb_tup in tb_name:
                                     	tb = "".join(tuple(tb_tup))
                                      	ReviewPart.ReviewPart().review_table(db,tb)
                                      	ReviewPart.ReviewPart().review_column(db,tb)
					ReviewPart.ReviewPart().review_extra(db,tb)
                             	rs_info = MySQL.MysqlQuery().query_select('select tb_name,tb_col,result from DB_REVIEW_CONTROL.tb_review_result where id > %s' %(max_id))
                              	if rs_info:
					review_status = 2
	                               	info = rs_info
                               	else:
					review_status = 1
                       	else:
				review_status = 3
		else:
			review_status = 4
               	try:
			LoadAndClean().moveFile(filepath)
			LoadAndClean().dropTmpDB(db)
              	except Exception,ex:
			print Exception,ex
		self.render('review.html',title='result_test',items=info,status=review_status)
		
class ReviewFile(tornado.web.RequestHandler):
	def post(self):
		now = time.localtime()
		str_now = time.strftime("%Y%m%d%H%M%S", now )
                review_status = 0
                info = []
		upload_path = os.path.join(os.path.dirname(__file__),'../tmp')


		if self.request.files['file']:
			file_metas = self.request.files['file']
			for meta in file_metas:
              			filename = meta['filename']
             			filepath = os.path.join(upload_path,filename+str_now)
           			with open(filepath,'wb') as up:
                  			up.write(meta['body'])
       	               		LoadAndClean().find_Load(filepath)
       				db = MySQL.tmpDB
              			max_id = MySQL.MysqlQuery().query_select('select max(id) from DB_REVIEW_CONTROL.tb_review_result')[0][0]
                		tb_name = MySQL.MysqlQuery().query_select('show tables from %s' %(db))
               			if tb_name:
                			for tb_tup in tb_name:
             					tb = "".join(tuple(tb_tup))
                				ReviewPart.ReviewPart().review_table(db,tb)
            					ReviewPart.ReviewPart().review_column(db,tb)    
              					ReviewPart.ReviewPart().review_extra(db,tb)     
            				rs_info = MySQL.MysqlQuery().query_select('select tb_name,tb_col,result from DB_REVIEW_CONTROL.tb_review_result where id > %s' %(max_id))
              				if rs_info:
            					review_status = 2
                				info = rs_info
              				else:
                				review_status = 1
             			else:
              				review_status = 3
           			try:
           				LoadAndClean().moveFile(filepath)
              				LoadAndClean().dropTmpDB(db)
              			except Exception,ex:
             				print Exception,ex
              	else:   
          		review_status = 4 
#           		try:
#           			LoadAndClean().moveFile(filepath)
#              			LoadAndClean().dropTmpDB(db)
#              		except Exception,ex:
#             			print Exception,ex
                self.render('review.html',title='result_test',items=info,status=review_status)

