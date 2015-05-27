import sys
from threading import Thread
from src.cpu_analysis import CpuAnalysis
from src.container_import import Container
from src.parse_xml import ParseXml

class mThread(Container):
	# counter => Numero de threads concorrentes/assincronas
	def __init__(self, metodo, argList, counter=1):
		parse = ParseXml()
		if len(argList) > 0:			
			if type(argList[0]) != int:
				if argList[0].has_key('id_login'):
					from src.bridge import Bridge
					bridge = Bridge()
				elif argList[0].has_key('test'):
					del argList[0]
					from src.bridge import Bridge
					bridge = Bridge()
					
		CPU = CpuAnalysis()
		num_cpus = CPU.num_cpus()
		if counter > num_cpus:
			counter = num_cpus
		try:
			if argList == []:
				t=Thread(target=eval(metodo[0]),args=())
				t.start()
				t.join()
			else:
				i=1
				for argName in argList:
					t=Thread(target=eval(metodo[0]),args=(argName,))
					if t.isAlive() == True:
						t.setDaemon(True)
					t.start()
					"""
					if i == counter:
						t.join()
						i=1
					else:
						i=i+1
					"""
		except Exception, e:
			self.log_msg("ERRO: mThread() "+str(e),"log.txt")
