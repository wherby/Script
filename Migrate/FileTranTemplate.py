import json
import httplib
from optparse import OptionParser
import logging
from pprint import pprint
import base64
import pickle

filename="C:\\Users\\zhoust\\Documents\\id.csv"

def readFile():
    global filename
    f=open(filename)
    lines=[]
    for line in f:
        pass

    f.close()

def main():
    
    readFile()


if __name__ != "__main__":
    print("This script can only be run in command line.")
    exit(-1)
else:
    main()
