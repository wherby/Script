# encoding: utf-8
import sys
#reload(sys) 
#sys.setdefaultencoding('utf8') 
import urllib,urllib2,re
import threading
from time import sleep,ctime
#from urllib2 import request
import os
import time
import threadpool

from Download2 import *
allfiles=[]


def downjpgmutithread( filepathlist, dir=""):
    

    print("total downloads: %d"%len(filepathlist)) 

    runlist=[]
    for file in filepathlist:
        runlist.append(([file,dir],None))
    print("start downloads")
    
    pool = threadpool.ThreadPool(5)
    reqs = threadpool.makeRequests(fileDownload, runlist)
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
	global allfiles
	for f in open('D:/TDDOWNLOAD/test/files.txt').readlines():
		allfiles.append(f.strip('\n'))
	downjpgmutithread(allfiles,'D:/TDDOWNLOAD/test/')