#!/usr/bin/env python
import sys, pprint, time, datetime, os, re, socket
from src.daemon import Daemon
from src.header_xml import HeaderXml
from src.mThread import mThread
from src.manager import Manager
from src.container_import import Container
from src.bridge import Bridge

# Global Vars
total_sub_arquivos = 10
arg_list_process = []

def get_arg_list():
	arg_list = []
	arg_dict = {}
	m = Manager()
	arr = m.get_xml_data()		
	for dados in arr:
		arg_dict['url'] = dados['url_xml']
		arg_dict['id_login'] = dados['id_login']
		arg_list.append(arg_dict)
		arg_dict = {}			
	return arg_list

#arg_list = ["http://www.google.com.br","http://www.terra.com.br","http://www.locaweb.com.br"]
#arg_list = ["http://www.ricardoeletro.com.br/Xml3/Index/250"]
#arg_list = [{"url":"http://www.passarela.com.br/parceiro/13.xml","id_login":"1820"},]
#arg_list = [{"url":"http://www.ricardoeletro.com.br/Xml3/Index/250","id_login":"3"},{"url":"http://www.ecolchao.com.br/Xml3/Index/142","id_login":"1842"},{"url":"http://www.passarela.com.br/parceiro/13.xml","id_login":"1820"},]
#arg_list = [{"url":"http://www.ricardoeletro.com.br/Xml3/Index/250","id_login":"3"},{"url":"http://www.ecolchao.com.br/Xml3/Index/142","id_login":"1842"},]	

# pega a ultima linha do arquivo com historico de modificacoes dos xmls
def get_last_modified_file(lib, path_file, last_modified):	
	if lib.file_exists(path_file):
		fp = lib.open_file(path_file,"r")
		lines_list = fp.readlines()
		lib.close_file(fp)
		last_line = lines_list[-1]
		return last_line
	else:
		return False
# faz o parse na ultima linha e compara com a info que vem do cabecalho,
# verifica o datetime do cabecalho eh maior que a do arquivo.
def parse_last_line(lib, last_modified, last_line):
	match = lib.preg_match("last-modified: (.*?) \|",last_line)
	if match != None:
		last_modified_line = match.group(1).replace("GMT","").strip()
		last_modified = last_modified.replace("GMT","").strip()
		last_modified_tm = time.mktime(datetime.datetime.strptime(last_modified, "%a, %d %b %Y %H:%M:%S").timetuple())
		last_line_tm = time.mktime(datetime.datetime.strptime(last_modified_line, "%a, %d %b %Y %H:%M:%S").timetuple())
		
		if last_modified_tm > last_line_tm:
			return True
		else:
			return False
	
# verifica se houve alteracao no xml
def gen_config_parse_file_c(lib, last_modified, dados):
	path_file = "/tmp/xml/last_modified_%s.txt" % (dados['id_login'])	
	last_line = get_last_modified_file(lib, path_file, last_modified)	
	if last_line != False:
		result = parse_last_line(lib, last_modified, last_line)
		if result == True:
			fp = lib.open_file(path_file,"a+")
			content = "last-modified: %s | url: %s\n"%(last_modified, dados['url'])
			lib.write_file(fp, content)
			lib.close_file(fp)
			return True
		else:
			return False
	else:
		fp = lib.open_file(path_file,"a+")
		content = "last-modified: %s | url: %s\n"%(last_modified, dados['url'])
		lib.write_file(fp, content)
		lib.close_file(fp)
		return True
# gera o arquivo com alguns dados do xml e do cliente, como, url, id_login e total de subarquivos
# para que a rotina em c, tenha parametros pra gerar os arquivos.
def gen_file_c(lib, dados):
	path_file = "/tmp/xml/"
	pfile = "xml_conf.txt"
	
	if not lib.file_exists(path_file):
		lib.__mkdir__(path_file)
		
	path_file = path_file+pfile
	fp = lib.open_file(path_file, "a+")
	content = "url: %s | id_login: %s | total_sub_arquivos: %d\n"%(dados['url'], dados['id_login'],total_sub_arquivos)
	file_content = fp.read()
	pattern = "id_login: "+str(dados['id_login'])
	match = lib.preg_match(pattern, file_content)
	if match == None:
		lib.write_file(fp, content)
	lib.close_file(fp)

# chama a rotina em c via socket, liberando para processar os xmls
def call_c_routine():
	try:
		HOST = 'localhost'
		PORT = int(sys.argv[3])
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((HOST, PORT))
		s.sendall('xml_liberado')
		data = s.recv(1024)
		s.close()
		return True
	except Exception, e:
		print "call_c_routine: Logar esse erro depois: ",e
		return False

# pega os dados de modificacao do arquivo, atraves de requisicao do cabecalho do arquivo.
def get_header_data():
	lib = Container()
	arg_list = get_arg_list()
	HX = HeaderXml()
	liberado = False
	for lista in arg_list:
		header = HX.get_header_data(lista['url'])
		if header != False:
			if header.has_key('last-modified'):
				gen_file = gen_config_parse_file_c(lib, header['last-modified'],lista)
				if gen_file == True:
					lista['tot'] = total_sub_arquivos
					arg_list_process.append(lista)
					liberado = True
					gen_file_c(lib, lista)
			else:
				print "Esses XML's, nao tem o campo 'last-modified', no cabecalho de requisicao: ",lista['url']
	if liberado == True:
		return call_c_routine()
	#return True
	
# Apos o xml ser processado pela rotina em C,
# chama o modulo pra gerar os csv's
def process_data():	
	bridge = Bridge()
	bridge.read_parse_xml(arg_list_process)
	return True
	
liberado = get_header_data()
if liberado == True:
	process_data()
	
"""
class MyDaemon(Daemon):
	def run(self):
		while True:
			get_header_data()
			time.sleep(10)
	
if __name__ == "__main__":
	pid_file = "/tmp/xml_parser.pid"
	daemon = MyDaemon(pid_file)

	if len(sys.argv) > 2:
		if 'start' == sys.argv[1]:
			daemon.start()
		elif 'stop' == sys.argv[1]:
			daemon.stop()
		elif 'restart' == sys.argv[1]:
			daemon.restart()
		else:
			print "Unknown command"
			sys.exit(2)
		sys.exit(0)
	else:
		print "usage: %s [start port] | [stop port] | [restart port] " % sys.argv[0]
		sys.exit(2)
		
	
	#metodo_list = ['bridge.test_thread_asynchronous']
	#arg_list = [{'test':True},1,2,3]
	#num_threads = len(arg_list)
	#mt = mThread
	#mt(metodo_list, arg_list, num_threads)
	
	#metodo_list = ['bridge.read_parse_xml']
	#arg_list = get_arg_list()
	
	#num_threads = len(arg_list)
	#mt = mThread
	#mt(metodo_list, arg_list, num_threads)
	"""
