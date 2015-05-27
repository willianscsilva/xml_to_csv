from src.mysqlconn import mysql_conn
from src.container_import import Container
class Manager(Container):
	
	def __init__(self):
		# Antes de ir para homologacao, passar os dados de acesso para um pickle		
		self.m = mysql_conn('localhost','user','pass','db')
		self.cursor = self.m.cursor
		
