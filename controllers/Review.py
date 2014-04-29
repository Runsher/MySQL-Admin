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

now = time.localtime()
str_now = time.strftime("%Y%m%d%H%M%S", now )

info = []
review_status = 0


class LoadAndClean():
	def find_Load(self,tmpfile):
#		for file in os.listdir("tmp/"):
#          	self.SqlTextIn="tmp/"+tmpfile
#            	MySQL.MysqlLoad().loadin(self.SqlTextIn)
            	MySQL.MysqlLoad().loadin(tmpfile)

	def moveFile(self,tmpfile):
		oldPath = tmpfile
		newPath =  os.path.join(os.path.dirname(__file__),'../sqlfile')
		shutil.move(oldPath,newPath)	

#	def del_tmp_file(self,tb):
#		tb_d = ['DB_REVIEW',"%s" %(tb)]
#		tb_del = '.'.join(tb_d)
#		tb_b = ['DB_REVIEW_BAK',"%s" %(tb)]
#		tb_bak = '.'.join(tb_b)
#		MySQL.MysqlQuery().query_update('drop table if exists %s' %(tb_bak))
#		MySQL.MysqlQuery().query_update('rename table %s to %s' %(tb_del,tb_bak))
		#MySQL.MysqlQuery().query_update('drop table if exists %s' %(tb_del)) 
	def dropTmpDB(self,db):
		MySQL.MysqlQuery().query_update('drop database %s' %(db))



class Review(tornado.web.RequestHandler):
	def get(self):
		self.render('review.html',title='result_test',items=info,status=review_status)


	def post(self):
		review_status = 0
                upload_path = os.path.join(os.path.dirname(__file__),'../tmp')  
		info = []
		dbTmpName = 'DB_TMP'+str_now
		file_me = self.get_argument('content')
		self.write(file_me)
		try:
                	file_metas = self.request.files['file']   
		except Exception,ex:
			print Exception,ex
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
		#				LoadAndClean().dropTmpDB(db)
                                        rs_info = MySQL.MysqlQuery().query_select('select tb_name,tb_col,result from DB_REVIEW_CONTROL.tb_review_result where id > %s' %(max_id))
                                        if rs_info:
						review_status = 2
	                                    	info = rs_info
                                                #for rs in rs_info:
                                                 #       info.append(rs[0])
                                        else:
						review_status = 1
                                else:
					review_status = 3
			else:
				review_status = 4
                      	try:
				LoadAndClean().moveFile(filepath)
				LoadAndClean().dropTmpDB(db)
                          #	for tb_del in tb_name:
                          #         	LoadAndClean().del_tmp_file(tb_del[0])
                      	except Exception,ex:
				print Exception,ex
		else:
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
		#	else:   
		#		review_status = 4 
				try:
					LoadAndClean().moveFile(filepath)
					LoadAndClean().dropTmpDB(db)
				#for tb_del in tb_name:
				#	LoadAndClean().del_tmp_file(tb_del[0])
				except Exception,ex:
                       			print Exception,ex
		self.render('review.html',title='result_test',items=info,status=review_status)
		#info = []
		
class Test(tornado.web.RequestHandler):
	def post(self):
		#items = ["Item 1", "Item 2", "Item 3"]
#		self.render("test.html", title="My title", items=items)
		#info = [('tb_avatar', '', '\xe4\xb8\x8d\xe5\xad\x98\xe5\x9c\xa8update\xe7\xb1\xbb\xe8\xae\xb0\xe5\xbd\x95\xe8\xa1\xa8\xe6\x95\xb0\xe6\x8d\xae\xe4\xbf\xae\xe6\x94\xb9\xe6\x97\xb6\xe9\x97\xb4\xe7\x9a\x84\xe5\xad\x97\xe6\xae\xb5'), ('tb_avatar', '', '\xe4\xb8\x8d\xe5\xad\x98\xe5\x9c\xa8create\xe7\xb1\xbb\xe8\xae\xb0\xe5\xbd\x95\xe8\xa1\xa8\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4\xe7\x9a\x84\xe5\xad\x97\xe6\xae\xb5\xef\xbc\x8c')]
#		info = [('test','中国')]
#		print info
#                review_status = 2
#                self.render('review.html',title='result_test',items=info,status=review_status)
		upload_path = os.path.join(os.path.dirname(__file__),'../tmp')
		file_metas = self.request.files['file']
		for meta in file_metas:
              		filename = meta['filename']
             		filepath = os.path.join(upload_path,filename+str_now)
           		with open(filepath,'wb') as up:
                  		up.write(meta['body'])

		print  file_metas 
