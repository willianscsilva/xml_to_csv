"""
Author: Willians Costa da Silva
Email: willianscsilva@gmail.com
License: GNU General Public License version 2.0 (GPLv2) - http://www.gnu.org/licenses/gpl-2.0.html
Created: 2013-03-23
Credits & Source:
- http://python.org/
Note: Copy, distribute, modify freely, but keep the credits, please.
"""
import MySQLdb
import sys,re

class mysql_conn():	 
	cursor,db = None,None
	def __init__(self,server, user, passwd, dbase):
		try:
			if (server!=None) and (user!=None) and (passwd!=None) and (dbase!=None):
				self.db = MySQLdb.connect(server, user, passwd, dbase, charset = "utf8", use_unicode = True )
				self.cursor = self.db.cursor()
		except Exception, e:
			msg = "Erro ao se conectar a base de dados! %s"%(e)
			print msg
			pass
		
	def load_array(self):
		obj_query = self.cursor		
		arr = []
		arr_assoc = {}            
		for line in [zip([ column[0] for column in obj_query.description], row) for row in obj_query.fetchall()]:			
			for data in line:				
				arr_assoc[data[0]] = data[1]                    
			arr.append(arr_assoc)
			arr_assoc = {}		
		return arr
