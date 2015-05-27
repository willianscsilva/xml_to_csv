import pycurl, StringIO, urllib2
from src.container_import import Container
class OpenUrl(Container):
	def __open__(self, url,ssl_verifypeer=False,cookie_file_name=None):
		try:
			buffer = StringIO.StringIO()
			c = pycurl.Curl()
			c.setopt( c.URL, url )
			c.setopt( c.USERAGENT,'Mozilla/5.0 (X11; Linux x86_64; rv:10.0.4) Gecko/20120425 Firefox/10.0.4')
			if ssl_verifypeer == False:
				c.setopt( c.SSL_VERIFYPEER, False )
			if cookie_file_name != None:
				c.setopt( c.COOKIEFILE,cookie_file_name )
				c.setopt( c.COOKIEJAR, cookie_file_name )
			c.setopt( c.WRITEFUNCTION, buffer.write )
			c.setopt( c.FOLLOWLOCATION, 1 )
			c.setopt( pycurl.VERBOSE, 1 )
			c.perform()
			c.close()
			content = buffer.getvalue()
			return content
		except Exception, e:
			self.log_msg("ERRO: __OpenUrl__.__open__() "+str(e),"log.txt")

	def stream(self, url):
		return urllib2.urlopen(url)
