import json
import httplib
from optparse import OptionParser
import logging
from pprint import pprint
import base64
import pickle

filename="C:\\Users\\zhoust\\Documents\\id.csv"
desfile="C:\\Users\\zhoust\\Documents\\id2.csv"

def readFile():
    global filename,desfile
    f=open(filename)
    lines=[]
    for line in f:
        fields1=line.split(',',5)
        fields2=fields1[5].rsplit(',',5)
        fields=fields1[0:5]+fields2
        if fields[5]=="":
            fields[5]=" "
        if fields[10]=="\n":
            fields[10]=" \n"
        #print "aaaa"+fields[10]+"bb"
        line=(",").join(fields)
        #print "kline "+line+"aaa"
        lines.append(line)
    
    print lines[0]
    f2=open(desfile,"w+")
    for line in lines:
        f2.write(line)
        #f2.write('/n')
    f2.close()
    f.close()



def main():
    
    readFile()


if __name__ != "__main__":
    print("This script can only be run in command line.")
    exit(-1)
else:
    main()
