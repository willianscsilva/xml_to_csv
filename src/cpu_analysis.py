import sys,os
from src.container_import import Container
class CpuAnalysis(Container):
	def num_cpus(self):
		try:
			return int(os.sysconf('SC_NPROCESSORS_ONLN'))
		except Exception , e:
			self.log_msg("ERRO: CpuAnalysis.num_cpus() "+str(e),"log.txt")
