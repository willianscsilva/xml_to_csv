import sys,os,codecs
class File:
	"""
	MODES:
		r: read only;
		rb: read only in binary format;
		r+: read and write, pointer beginning of the file;
		rb+: read and write binary format;
		w: write only, overwrite file if exists;
		wb: write only in binary format; 
		w+: write and read, overwrite file if exists;
		wb+: write and read in binary format, overwrite file if exists;
		a: Opens a file for appending. The file pointer is at the end of the file if the file exists;
		ab: Opens a file for appending in binary format. The file pointer is at the end of the file if the file exists; 
		a+: Opens a file for both appending and reading. The file pointer is at the end of the file if the file exists;
		ab+: pens a file for both appending and reading in binary forma;t
	"""	
	path_file = "/tmp/xml"
	path_file_csv = "/tmp/csv"
	def open_file(self,path,mode='w',encode=None):
		if encode == None:
			file_p = open(path,mode)
		else:
			file_p = codecs.open(path,encoding='utf-8',mode='w')
		return file_p
		
	def get_file_size(self, file_name=None, file_p=None):		
		fclose = False
		if file_name != None:
			file_name = self.get_path_xml(file_name)
			file_p = self.open_file(file_name,"r")
			fclose = True
		file_p.seek(0,2)
		size = file_p.tell()
		if fclose == True:
			self.close_file(file_p)
		return size

	def write_file(self,file_p,text):
		file_p.write(text)

	def close_file(self,file_p):
		file_p.close()

	def remove_file(self,path):
		if os.path.exists(path):
			os.remove(path)
		
	def file_exists(self,path):
		if os.path.exists(path):
			file_size = os.path.getsize(path)
			if file_size > 0:
				return True
			else:
				return False
		else:
			return False
			
	def __mkdir__(self, path):
		os.mkdir(path)
	
	def real_path(self):
		return os.path.realpath(os.path.dirname(__file__)+'/')
		
	def get_path_xml(self, name):
		file_name = "%s.xml"%(name)
		return "%s/%s"%(self.path_file, file_name)
		
	def get_path_csv(self, name):
		file_name = "%s.csv"%(name)
		return "%s/%s"%(self.path_file_csv, file_name)
		
