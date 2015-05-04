# encoding: utf-8
import sys
#reload(sys) 
#sys.setdefaultencoding('utf8') 
import urllib,urllib2,re
import threading
from time import sleep,ctime
#from urllib2 import request
import confForWeb
import os
import time
import socket

socket.setdefaulttimeout(20)

rooturl=confForWeb.rooturl
sigurl =confForWeb.sigurl
distdir=confForWeb.distdir
prefixurl=confForWeb.prefixurl
minumPic=confForWeb.minumPic
allfiles=[]


def get_rootPage(url):
    global prefixurl
    content=""
    try:
        content = urllib.urlopen(url).read()
    except  Exception as e:
        print e
    #content=content.encode("utf-8")
    
    links=re.findall(r'<h3><a href=\"htm_data(\S*)\"',content)
    print "total links :"+str(len(links))
    for line in links:
        tline=prefixurl+line
        print tline
        get_singlePage(tline)
        time.sleep(2)
    #print links
    #print content


def get_singlePage(url):
    content=""
    try:
        content = urllib.urlopen(url).read()
    except  Exception as e:
        print e
    links=re.findall(r'<input type=\'image\' src=\'(\S*)\'',content)
    ll=[]
    for line in links:
        #print line
        tline=str(line)
        ll.append(tline)
    downjpgmutithread(ll)
    print ll


def downjpg( filepath ):
    global allfiles

    try:
        name=filepath[filepath.rfind('/')+1:]
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = { 'User-Agent' :user_agent }
        
        req = urllib2.Request(filepath)
        req.add_header('User-Agent', user_agent);
        req.add_header('accept', '*/*');
        req.add_header('connection', 'keep-alive');
        req.add_header('Content-Type', 'text/plain')
        web =urllib2.urlopen(filepath)
        
 
            
        print("visit net work file: "+filepath+"\n")
        DstDir=distdir
        print("save file to :"+DstDir+name)
        destfile=DstDir+name
        downloaded = 0

            
        try:
            print destfile
            fp = open(destfile, "wb")
            r = web.read()
            web.close()
            print len(r)
            fp.write(r)
            print "finish"
        except  Exception as e:
            print e
            #print "write error"
            #print type(e)
            #print e.args
        finally:
            fp.close()
    except  Exception as e:
        print e

            


def downjpgmutithread( filepathlist ):
    global allfiles,minumPic
    if len(filepathlist) < minumPic:
        return
    print("共有%d个文件需要下载"%len(filepathlist)) 
    for file in filepathlist:
        print( file )
    runlist=[]
    for file in filepathlist:
        name=file[file.rfind('/')+1:]
        if allfiles.count(name)==0:
            runlist.append(file)
            
    print("single thread")
    print runlist
    for file in runlist:
        downjpg(file)

    print("已经完成所有任务")

testFile=["https://40.media.tumblr.com/a84df946bb76ba31a242a95e049ace44/tumblr_nnrajmdjPR1u37z5fo1_540.jpg"]
if __name__ =='__main__':
    for root,dirs,files in os.walk(distdir):
        for file in files:
            allfiles.append(file)
    #downjpg(testFile[0])
    #print allfiles
    #get_singlePage(sigurl)
    get_rootPage(rooturl)
