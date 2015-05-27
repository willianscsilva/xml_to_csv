import urllib2
class HeaderXml:
	request = None
	def __init__(self):
		pass
		
	def get_header_data(self,url):
		try:
			request = urllib2.Request(url)
			opener = urllib2.build_opener()
			firstdatastream = opener.open(request)
			header = firstdatastream.headers.dict
			return header
		except Exception, e:
			print "get_header_data: Logar esse erro depois: url: %s, ERRO: %s\n"%(url, e)
			return False
