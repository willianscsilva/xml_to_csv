import urllib2
import sys

def header__():

        request = urllib2.Request(sys.argv[1])
 	opener = urllib2.build_opener()
	firstdatastream = opener.open(request)
	header = firstdatastream.headers.dict
	if header.has_key('last-modified'):
		return header['last-modified']
	else:
	        return False

if __name__ == "__main__":
        print header__()
