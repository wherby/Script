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
import threadpool

rooturl=confForWeb.rooturl
sigurl =confForWeb.sigurl
distdir=confForWeb.distdir
prefixurl=confForWeb.prefixurl
minumPic=confForWeb.minumPic
allfiles=[]


def get_rootPage(url):
    global prefixurl
    content = urllib.urlopen(url).read()
    #content=content.encode("utf-8")
    
    links=re.findall(r'<h3><a href=\"htm_data(\S*)\"',content)
    for line in links:
        tline=prefixurl+line
        print tline
        get_singlePage(tline)
        time.sleep(2)
    #print links
    #print content


def get_singlePage(url):
    content = urllib.urlopen(url).read()
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
        web = urllib.urlopen( filepath)
        print("visit net work file: "+filepath+"\n") 
        jpg = web.read()
        DstDir=distdir
        print("save file to :"+DstDir+name)
        try:
            File = open( DstDir+name,"wb" )
            File.write( jpg)
            File.close()
            return
        except IOError:
            print("write file error\n")
            return
    except Exception as e:
        print e
        
        return 

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
            runlist.append(filepathlist)
    print("开始多线程下载")
    
    pool = threadpool.ThreadPool(5)
    reqs = threadpool.makeRequests(downjpg, runlist)
    [pool.putRequest(req) for req in reqs]
    pool.wait()
    '''
    task_threads=[] #存储线程
    count=1
    for file in filepathlist:
        name=file[file.rfind('/')+1:]
        if allfiles.count(name)>0:
            print "file aready saved."
            continue
        print "file name :"+file
        t= threading.Thread( target=downjpg,args=(file,) )
        count=count+1
        task_threads.append(t)
    for task in task_threads:
        task.start()
        #time.sleep(5)
    for task in task_threads:
        task.join() #等待所有线程结束
    '''
    print("已经完成所有任务")
    
if __name__ =='__main__':
    for root,dirs,files in os.walk(distdir):
        for file in files:
            allfiles.append(file)

    #print allfiles
    get_singlePage(sigurl)
    #get_rootPage(rooturl)
