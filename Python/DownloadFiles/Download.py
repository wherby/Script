import urllib
from retry import *
import urllib2

@retry(urllib2.URLError, tries=4, delay=3, backoff=2)
def fileDownload(filename,dir=""):
	desFile=dir + filename.split('/')[-1]
	urllib.urlretrieve(filename , desFile)


if __name__ =='__main__':
	fileDownload('http://download.thinkbroadband.com/10MB.zip')