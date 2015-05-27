import sys,time
from src.file import File
class Log(File):	
	def get_path_file_log(self):
		path = self.real_path()
		return "%s/log"%(path)
		
	def log_msg(self, msg, name):
		path_log = self.get_path_file_log()
		if not self.file_exists(path_log):
			self.__mkdir__(path_log)
		
		file_log = "%s/%s"%(path_log,name)
		fp = self.open_file(file_log,'a')
		separator = "#"*100
		msg = "%s\n%s\n%s\n"%(separator, msg, separator)
		self.write_file(fp,msg)
		self.close_file(fp)
