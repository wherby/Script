import urllib2
from retry import *
url = "http://download.thinkbroadband.com/10MB.zip"

@retry(urllib2.URLError, tries=4, delay=3, backoff=2)
def readBlock(u,block_sz):
	return u.read(block_sz)

def fileDownload(url,dir=""):
	fname = url.split('/')[-1]
	file_name = dir + url.split('/')[-1]
	u = urllib2.urlopen(url)
	f = open(file_name, 'wb')
	meta = u.info()
	file_size = int(meta.getheaders("Content-Length")[0])
	print "Downloading: %s Bytes: %s" % (file_name, file_size)

	file_size_dl = 0
	block_sz = 8192 * 40
	while True:
	    buffer =readBlock(u,block_sz)
	    if not buffer:
	        break

	    file_size_dl += len(buffer)
	    f.write(buffer)
	    status = r"%10d  [%3.2f%%]   %s" % (file_size_dl, file_size_dl * 100. / file_size, fname)
	    status = status + chr(8)*(len(status)+1)
	    print status,

	f.close()

if __name__ =='__main__':
	fileDownload('http://download.thinkbroadband.com/10MB.zip')