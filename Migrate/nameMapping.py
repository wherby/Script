import json
import httplib
from optparse import OptionParser
import logging
from pprint import pprint
import base64
import pickle

l1=[]

rec={}

def readFile():
    global l1
    f=open("C:\\Users\\zhoust\\Documents\\Columbus.txt",'r')
    for line in f:
        l1.append(line.lstrip(' ').rstrip('\n'))
        
    l1= filter(lambda x:len(x)!=0,l1)
    l1=filter(lambda x:x.find("------------")==-1,l1)
    l1=filter(lambda x:x.find("affected)")==-1,l1)
    l1=filter(lambda x:x.find("firstname             lastname")==-1,l1)
    pprint(l1)
    print len(l1)

    for line in l1:
        b=line.split(' ')
        b=filter(lambda x: len(x)!=0,b)
        id,fn,ln=b
        name=fn+" "+ln
        if rec.has_key(name):
            rec[name].append(id)
        else:
            rec[name]=[id]
    pprint(rec)
    f.close()

    f=open("C:\\Users\\zhoust\\Documents\\oxygen.txt",'w')
    pickle.dump(rec,open("C:\\Users\\zhoust\\Documents\\oxygen.p",'wb'))
    pprint(rec,f)
    f.close()
    




def main():
    print "start....."


    readFile()

    

if __name__ != "__main__":
    print("This script can only be run in command line.")
    exit(-1)
else:
    main()
