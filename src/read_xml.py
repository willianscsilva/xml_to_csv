from src.open_url import OpenUrl
from src.container_import import Container
from ctypes import *
import re,sys
class ReadXml(Container):
	def __init__(self):
		self.open_url = OpenUrl()		
		
	def __read__(self,url):
		try:
			xml_content = self.open_url.__open__(str(url))
			xml_content_p = c_char_p(xml_content)
			return xml_content_p
		except Exception, e:			
			self.log_msg("ERRO: ReadXml.__read__() "+str(e),"log.txt")

	def read_from_xml_file(self, nome):
		try:
			result = {}
			xml_file = self.get_path_xml(nome)			
			fp = self.open_file(xml_file,"r")
			"""
			i=0
			for line in fp:				
				line_p = c_char_p(line)
				if self.count_line_break(line_p) > 0:
					#result['multiline'] = True						
					result['multiline'] = False
					result['content_pointer'] = line_p
				else:
					result['multiline'] = False
					result['content_pointer'] = line_p					
				i=i+1
			"""
			content = fp.read()
			self.close_file(fp)
			line_p = c_char_p(content)
			line_p = self.remove_line_break(line_p)			
			result['multiline'] = False
			result['content_pointer'] = line_p
			return result
		except Exception, e:
			self.log_msg("ERRO: ReadXml.read_from_xml_file() "+str(e),"log.txt")
			
	def count_line_break(self, line_pointer):
		try:
			line = line_pointer.value
			pt_compile = re.compile('\n',re.IGNORECASE)
			result = re.findall(pt_compile,line)		
			if result != None:						
				sum=0
				for res in result:
					sum=sum+len(res)	
				return sum		
			else:
				return 0
		except Exception, e:
			self.log_msg("ERRO: ReadXml.count_line_break() "+str(e),"log.txt")
			
	def remove_line_break(self, data):
		qtd_line_break = self.count_line_break(data)		
		if qtd_line_break > 0:			
			data.value = data.value.replace("\n", "")
		return data
