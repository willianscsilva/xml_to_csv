import Queue, socket
from threading import Thread
from src.open_url import OpenUrl
from src.container_import import Container
from src.read_xml import ReadXml
from src.mThread import mThread
from src.xml_config import XmlConfig

from ctypes import *
import sys,gc,pprint
sys.setrecursionlimit(1000000)
gc.enable()
class Bridge(Container):
	tot = 6
	block_pointer = None
	def teste_thread(self, url):
		OpU = OpenUrl()
		OpU.__open__(url)
		
	def teste_pointer(self):
		s = "Hello, World"
		c_s = c_char_p(s)
		print c_s.value
		
	def test_thread_asynchronous(self,val):
		list_s = []
		n = 10
		list_s.append(n*val)
		print list_s
		
	def read_parse_xml(self, dados):
		args = {}
		arg_list = []		
		X = XmlConfig()
		read_xml = ReadXml()
		
		# Descomentar isso depois dos testes
		"""
		msg = self.read_socket()		
		if msg == "sub_arquivos_liberados":
			print "Estamos liberados para gerar o csv!\n"
		else:	
			print "Nao recebemos a liberacao, apenas uma msg., MSG: ",msg
			return False
		"""
		
		for data in dados:
			self.tot = data['tot']
			arr_config = X.get_data(str(data['id_login']))
			if arr_config != False:
				arr_config[0]['ordem_campos_xml'] = arr_config[0]['ordem_campos_xml']+",mounth"+",amount"
				# Abrir a url dos xmls e gerar os subarquivos, foram portadas para linguagem C				
				"""
				# xml_pointer = read_xml.__read__(dados['url'])
				# Se tem quebra de linha, entre as tags, tira todas.			
				tot_bl = read_xml.count_break_line(xml_pointer)
				if tot_bl > 0:
					xml_pointer.value = xml_pointer.value.replace("\n","")
				"""
				for i in range(1,self.tot+1):
					nome = "XML_%s_%s"%(data['id_login'],i)
					file_size = self.get_file_size(nome)
					if file_size > 0:
						print "NOME ", nome, " id_login ", data['id_login']
						args = read_xml.read_from_xml_file(nome)
						args['id_login'] = data['id_login']
						args['config_xml'] = arr_config[0]
						arg_list.append(args)
				
				if arg_list != []:
					metodo_list = ['parse.switch']							
					mt = mThread
					mt(metodo_list, arg_list, self.tot)
				arg_list = []
				args = {}
				
	
	def read_socket(self):
		try:
			print "Aguardando dados via socket..."
			HOST = 'localhost'            # Symbolic name meaning all available interfaces
			PORT = int(sys.argv[2])       # Arbitrary non-privileged port
			msg = ""
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.bind((HOST, PORT))
			s.listen(1)
			conn, addr = s.accept()
			print 'Connected by', addr
			while 1:
				data = conn.recv(1024)				
				if not data: break
				msg = data
				conn.sendall(data)
			conn.close()			
			return msg
		except Exception, e:
			print "read_socket: Logar esse erro depois, ERRO: %s\n"%(e)
			return False
	
	# As rotinas daqui pra baixo, foram portadas para linguagem C	
	def gen_xml_file(self, xml_pointer, id_login):
		read_xml = ReadXml()		
		xml_file = self.get_path_xml(id_login)		
		self.gen_file(xml_file,xml_pointer)		
	
	def gen_file(self,xml_file,xml_pointer):
		block_plist = []
		inicio = 0
		division_string = len(xml_pointer.value)/self.tot		
		fim = division_string
		xml_file_novo = ""
		
		q = Queue.Queue()		
		#block_pointer = self.get_block_struct(xml_pointer, inicio, division_string, 0)
		t=Thread(target=self.get_block_struct,args=(xml_pointer, inicio, division_string, 0, q,))				
		t.start()		
		block_pointer = q.get()
		block_plist.append(block_pointer)
		for i in range(self.tot-1):
			q = Queue.Queue()
			inicio = inicio + division_string
			fim = fim+division_string
			#block_pointer = self.get_block_struct(xml_pointer, inicio, fim, 0)			
			t=Thread(target=self.get_block_struct,args=(xml_pointer, inicio, fim, 0, q,))				
			t.start()
			block_pointer = q.get()
			block_plist.append(block_pointer)
		
		if not self.file_exists(self.path_file):
			self.__mkdir__(self.path_file)
			
		arr_nome_xml = xml_file.split(".")
		i = 1
		for block in block_plist:
			#Expl.: 3_1.xml
			xml_file_novo = ("%s_%s.%s") % (arr_nome_xml[0], str(i), arr_nome_xml[1])
			if self.file_exists(xml_file_novo):
				self.remove_file(xml_file_novo)
			
			fp = self.open_file(xml_file_novo,"w")		
			self.write_file(fp,block.value)		
			self.close_file(fp)
			i=i+1
			xml_file_novo = ""
			
	def get_block_struct(self, xml_pointer, inicio, fim, iterat, q):
		end_block, content = None, None
		iterat_interno=0
		if iterat != 0:
			iterat_interno = iterat
			
		if iterat_interno != 0:
			iterat_interno = iterat_interno+1		
			end_block = xml_pointer.value[inicio:fim+iterat_interno][-10:]
			content = xml_pointer.value[inicio:fim+iterat_interno]
		else:
			end_block = xml_pointer.value[inicio:fim][-10:]
			content = xml_pointer.value[inicio:fim]
			
		#print "BLOCK ",end_block
		#print "INICIO ",inicio," FIM ",fim 
		
		result = self.preg_match('\/item>|\/rss>',end_block)
		if result == None:
			if iterat_interno > 1:					
				if content != None and end_block != None:
					del end_block, content
					end_block, content = None, None				
				#return self.get_block_struct(xml_pointer, inicio, fim, iterat_interno)
				#self.get_block_struct(xml_pointer, inicio, fim, iterat_interno, q)
				t=Thread(target=self.get_block_struct,args=(xml_pointer, inicio, fim, iterat_interno, q,))				
				t.start()
			else:
				if content != None and end_block != None:
					del end_block, content
					end_block, content = None, None
				#return self.get_block_struct(xml_pointer, inicio, fim, 1)
				#self.get_block_struct(xml_pointer, inicio, fim, 1, q)
				t=Thread(target=self.get_block_struct,args=(xml_pointer, inicio, fim, 1, q,))				
				t.start()
		else:
			q.put(c_char_p(content))
			#return c_char_p(content)
